import csv
import utils
import faiss
import numpy as np

from math import ceil
from weights import (
    CATEGORY_WEIGHTS,
    SECTION_WEIGHTS,
    CANDIDATE_PENALTY,
    REDROB_SIGNAL_WEIGHTS,
    OVERALL_WEIGHTS,
)
from typing import Dict, List
from collections import defaultdict
from utils.candidate import Candidate, ReasonFeatures
from utils import (
    load_json_file,
    parse_args,
    debug,
    path,
)


@debug
def accumulate_chunks():
    import os
    import json

    with open("./chunks_data.json", "r") as fp:
        chunks_data = json.load(fp)

    for target_file, chunks in chunks_data.items():
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "wb") as fp:
            for chunk in chunks:
                with open(chunk, "rb") as cp:
                    fp.write(cp.read())


@debug
def clean_loaded_chunks():
    import os
    import json

    with open("./chunks_data.json", "r") as fp:
        chunks_data = json.load(fp)

    for target_file in chunks_data.keys():
        if not (os.path.exists(target_file) and os.path.isfile(target_file)):
            continue
        os.remove(target_file)


@debug
def load_candidates(file: str) -> Dict[str, Dict]:
    decode = __import__("msgspec").json.decode
    with (
        __import__("gzip").open(file, "rb")
        if path.basename(file).endswith(".gz")
        else open(file, "rb")
    ) as fp:
        return {
            c.candidate_id: {
                "candidate": c,
                "embedded": {
                    "sources": c.embed_data,
                    "vectors": {
                        "summary": None,
                        "skills": [],
                        "experience": [],
                    },
                },
            }
            for c in (decode(line, type=Candidate) for line in fp)
        }


@debug
def load_job_desc(file: str) -> Dict[str, np.ndarray]:
    return {
        section: np.array(vectors)
        for section, vectors in load_json_file(file).items()  # type: ignore
    }


def retrieve(index, lookup, queries, k=2000):
    # Performing retrieval and accumulating hits for candidates
    D, I = index.search(queries, k)  # noqa: E741
    candi_hits = defaultdict(list)
    for row in range(len(queries)):
        for idx, distance in zip(I[row], D[row]):
            if idx == -1:
                continue
            cid = lookup[idx]["cid"]
            candi_hits[cid].append(float(distance))
    return candi_hits


@debug
def build_jd_query(processed):
    # Building JD Query for re-ranking
    must_have = " ".join(processed["must_have"])
    core = " ".join(processed["core_ml_retrieval"] + processed["evaluation_ml_depth"])
    context = " ".join(processed["context"] + processed["execution_signal"])
    return (f"ROLE: \n{must_have}\n\nSKILLS: \n{core}\n\nCONTEXT: \n{context}").strip()


@debug
def rerank(query: str, model, candis: List[Candidate]):
    # Running the re-ranker and returning scores
    texts = (candi.text for candi in candis)
    pairs = [(query, t) for t in texts]

    scores = model.predict(pairs, batch_size=32)
    ranked_idx = np.argsort(scores)[::-1]
    return {candis[idx].candidate_id: float(scores[idx]) for idx in ranked_idx}


def score_candidate(candi):
    """
    Score a candidate and accumulate reason features for robust reason generation.

    NOTE: This function signature has changed. It now takes only the candidate wrapper dict
    and accesses both the candidate object and its embedded vectors internally.

    The scoring data (retrieval results) should be pre-computed and stored in the wrapper.

    Returns: total_score (float)
    Side effect: populates candidate._reason_features
    """
    candidate = candi["candidate"]
    data = candi.get("retrieval_data", {})

    skills_vecs = candi["embedded"]["vectors"]["skills"]
    exp_vecs = candi["embedded"]["vectors"]["experience"]
    summary_vec = candi["embedded"]["vectors"]["summary"]

    # Initialize reason features
    features = ReasonFeatures()
    features.yoe = candidate.profile.years_of_experience
    features.current_title = candidate.profile.current_title
    features.current_company = candidate.profile.current_company
    features.current_industry = candidate.profile.current_industry
    features.past_titles = [c.title for c in candidate.career_history[1:]]
    features.past_industries = list(
        set(c.industry for c in candidate.career_history[1:])
    )
    features.profile_completeness = candidate.redrob_signals.profile_completeness_score
    features.is_verified = (
        candidate.redrob_signals.verified_email
        and candidate.redrob_signals.verified_phone
    )
    features.is_active = candidate.redrob_signals.profile_views_received_30d > 10
    features.open_to_work = candidate.redrob_signals.open_to_work_flag
    features.response_rate = candidate.redrob_signals.recruiter_response_rate
    features.github_active = candidate.redrob_signals.github_activity_score > 0

    # Count skills
    features.relevant_skill_count = len(candidate.skills)
    features.advanced_skill_count = sum(
        1 for s in candidate.skills if s.proficiency == "advanced"
    )
    features.top_skills = [s.name for s in candidate.skills[:5]]

    assessments = candidate.redrob_signals.skill_assessment_scores
    if assessments:
        features.skill_assessment_avg = np.mean(list(assessments.values()))

    # Finding centroid of vectors
    skills_c = utils.centroid(skills_vecs) if skills_vecs else None
    exp_c = utils.centroid(exp_vecs) if exp_vecs else None

    # Initial Retrieval Score
    match_score = 0.0
    top_sections = []

    for category, sections in data.items():
        category_weight = CATEGORY_WEIGHTS.get(category, 1.0)

        for section, distances in sections.items():
            section_weight = SECTION_WEIGHTS.get(section, 1.0)

            similarities = list(
                sorted((utils.cosine_from_l2(d) for d in distances), reverse=True)
            )
            signal = similarities[0]

            if len(similarities) > 1:
                signal += 0.25 * similarities[1]
            if len(similarities) > 2:
                signal += 0.25 * similarities[2]

            match_score += signal * category_weight * section_weight

            # Track top matching sections for reason
            if similarities:
                top_sections.append((section, similarities[0]))

    features.match_score = match_score
    features.top_matching_sections = [
        s[0] for s in sorted(top_sections, key=lambda x: x[1], reverse=True)[:3]
    ]

    # Determine match category
    if match_score >= 0.7:
        features.match_category = "high"
    elif match_score >= 0.4:
        features.match_category = "medium"
    else:
        features.match_category = "low"

    # Check if current/past roles are relevant (simplified check)
    features.has_relevant_current_role = features.match_category == "high"
    features.has_relevant_past_role = any(
        s[0] in ("experience", "skills") for s in top_sections[:3]
    )

    # Internal mismatch scoring
    penalty = 0.0
    penalty_breakdown = {}

    if skills_c is not None and exp_c is not None:
        similarity = utils.cosine_similarity(skills_c, exp_c)
        p = (1 - similarity) * CANDIDATE_PENALTY["skills_experience_mismatch"]
        penalty += p
        penalty_breakdown["skills_experience_mismatch"] = p

    if summary_vec is not None and exp_c is not None:
        similarity = utils.cosine_similarity(summary_vec, exp_c)
        p = (1 - similarity) * CANDIDATE_PENALTY["summary_experience_mismatch"]
        penalty += p
        penalty_breakdown["summary_experience_mismatch"] = p

    if summary_vec is not None and skills_c is not None:
        similarity = utils.cosine_similarity(summary_vec, skills_c)
        p = (1 - similarity) * CANDIDATE_PENALTY["summary_skills_mismatch"]
        penalty += p
        penalty_breakdown["summary_skills_mismatch"] = p

    features.internal_penalty = penalty
    features.penalty_breakdown = penalty_breakdown

    # Analyze skill source
    skill_source, _ = candidate._analyze_skill_sources()
    features.skill_source = skill_source

    # Redrob signal matching
    redrob_score = 0.0
    for signal, weight in REDROB_SIGNAL_WEIGHTS.items():
        redrob_score += weight * getattr(candidate.redrob_signals, signal)

    total_score = (
        OVERALL_WEIGHTS["match"] * match_score
        + OVERALL_WEIGHTS["penalty"] * penalty
        + OVERALL_WEIGHTS["redrob"] * redrob_score
    )

    # Store features on candidate for reason generation
    candidate._reason_features = features

    return total_score


@debug
def main(candidates_file: str, output_path: str):
    accumulate_chunks()

    # Loading & Building Data -----------------------------------------------------
    candidates: Dict[str, Dict] = load_candidates(candidates_file)

    job_desc = load_job_desc("./processed/job_desc.json")

    summary_vectors = np.load("./processed/summary_vectors.npy")
    skills_vectors = np.load("./processed/skills_vectors.npy")
    experience_vectors = np.load("./processed/experience_vectors.npy")

    summary_index = faiss.read_index("./processed/summary_index.faiss")
    skills_index = faiss.read_index("./processed/skills_index.faiss")
    experience_index = faiss.read_index("./processed/experience_index.faiss")

    summary_lookup = load_json_file("./processed/summary_lookup.json")
    skills_lookup = load_json_file("./processed/skills_lookup.json")
    experience_lookup = load_json_file("./processed/experience_lookup.json")

    for idx, entry in enumerate(summary_lookup):
        candidates[entry["cid"]]["embedded"]["vectors"]["summary"] = summary_vectors[
            idx
        ]

    for idx, entry in enumerate(skills_lookup):
        candidates[entry["cid"]]["embedded"]["vectors"]["skills"].append(
            (skills_vectors[idx], entry["idx"])
        )

    for idx, entry in enumerate(experience_lookup):
        candidates[entry["cid"]]["embedded"]["vectors"]["experience"].append(
            (experience_vectors[idx], entry["idx"])
        )

    for candi in candidates.values():
        candi["embedded"]["vectors"]["skills"] = list(
            map(
                lambda x: x[0],
                sorted(candi["embedded"]["vectors"]["skills"], key=lambda x: x[1]),
            )
        )
        candi["embedded"]["vectors"]["experience"] = list(
            map(
                lambda x: x[0],
                sorted(candi["embedded"]["vectors"]["experience"], key=lambda x: x[1]),
            )
        )

    # Initial Retrieval ----------------------------------------------------------
    retrieval_results = {
        section: {
            "summary": retrieve(summary_index, summary_lookup, queries),
            "skills": retrieve(skills_index, skills_lookup, queries),
            "experience": retrieve(experience_index, experience_lookup, queries),
        }
        for section, queries in job_desc.items()
    }

    # Store retrieval data in candidate wrappers for score_candidate to use
    for section, result in retrieval_results.items():
        for category, candis in result.items():
            for cid, distances in candis.items():
                if "retrieval_data" not in candidates[cid]:
                    candidates[cid]["retrieval_data"] = {}
                if category not in candidates[cid]["retrieval_data"]:
                    candidates[cid]["retrieval_data"][category] = {}
                if section not in candidates[cid]["retrieval_data"][category]:
                    candidates[cid]["retrieval_data"][category][section] = []
                candidates[cid]["retrieval_data"][category][section].extend(distances)

    # Initial ranking --------------------------------------------------------------
    candi_scores = dict(
        sorted(
            ((cid, score_candidate(candidates[cid])) for cid in candidates.keys()),
            key=lambda x: x[1],
        )
    )

    print("importing sentence_transformers (this may take long)")
    from sentence_transformers import CrossEncoder  # noqa: E402

    print("sentence_transformers imported")

    # Reranking
    reranker_scores = rerank(
        build_jd_query(utils.job_desc.processed),
        CrossEncoder("./models/ms-marco-MiniLM-L-12-v2"),
        [candidates[cid]["candidate"] for cid in list(candi_scores.keys())[:200]],
    )

    # Accumulation
    for cid, score in reranker_scores.items():
        candi_scores[cid] += score * OVERALL_WEIGHTS["reranker"]

    # Normalizing
    _max_score = ceil(max(list(candi_scores.values())))

    normalized = {
        cid: round(score / _max_score, 4) for cid, score in candi_scores.items()
    }

    # Final Sorting
    ranked = sorted(normalized.items(), key=lambda x: (-x[1], x[0]), reverse=False)

    # Saving
    with open(output_path, "w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(("candidate_id", "rank", "score", "reasoning"))
        writer.writerows(
            (cid, rank, score, candidates[cid]["candidate"].reason)
            for rank, (cid, score) in enumerate(ranked[:100], 1)
        )


if __name__ == "__main__":
    main(
        **parse_args(
            candidates_file="candidates.jsonl",
            output_path="submission.csv",
        )
    )
    clean_loaded_chunks()
