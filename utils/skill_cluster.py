import re
import numpy as np
from typing import Dict, List
from collections import defaultdict

from . import debug


# =============================================================================
# CONFIGURATION
# =============================================================================
SKILL_CLUSTER_MAP = {
    "software_engineering": [
        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "Go",
        "Rust",
        "Node.js",
        "Django",
        "Flask",
        "FastAPI",
        "Spring Boot",
        "gRPC",
        "REST APIs",
        "Microservices",
        "GraphQL",
        "Next.js",
        "React",
        "Redux",
        "Vue.js",
        "HTML",
        "CSS",
        "Tailwind",
        "Webpack",
    ],
    "data_engineering": [
        "Spark",
        "Airflow",
        "Kafka",
        "Apache Flink",
        "Apache Beam",
        "Databricks",
        "ETL",
        "Data Pipelines",
        "dbt",
        "Snowflake",
        "BigQuery",
        "Hadoop",
    ],
    "retrieval_ranking": [
        "BM25",
        "Elasticsearch",
        "OpenSearch",
        "FAISS",
        "Pinecone",
        "Weaviate",
        "Qdrant",
        "Milvus",
        "Vector Search",
        "Recommendation Systems",
        "Information Retrieval",
        "Haystack",
    ],
    "machine_learning": [
        "Feature Engineering",
        "XGBoost",
        "Statistical Modeling",
        "Forecasting",
        "scikit-learn",
        "Machine Learning",
        "Data Science",
    ],
    "deep_learning": [
        "PyTorch",
        "TensorFlow",
        "CNN",
        "GANs",
        "Object Detection",
        "Image Classification",
        "YOLO",
        "OpenCV",
        "Computer Vision",
        "Deep Learning",
        "Reinforcement Learning",
    ],
    "nlp_llm": [
        "NLP",
        "Hugging Face Transformers",
        "Fine-tuning LLMs",
        "LoRA",
        "PEFT",
        "Prompt Engineering",
        "LangChain",
        "Sentence Transformers",
        "Embeddings",
        "Speech Recognition",
        "TTS",
    ],
    "mlops": [
        "BentoML",
        "MLflow",
        "Kubeflow",
        "Weights & Biases",
        "MLOps",
        "CI/CD",
    ],
    "cloud": [
        "AWS",
        "Azure",
        "GCP",
        "Kubernetes",
        "Docker",
        "Terraform",
    ],
    "database": [
        "SQL",
        "PostgreSQL",
        "MongoDB",
        "Redis",
    ],
    "frontend": [
        "Angular",
        "Figma",
        "Illustrator",
        "Photoshop",
    ],
    "domain": [
        "Marketing",
        "Sales",
        "Salesforce CRM",
        "Accounting",
        "Tally",
        "SAP",
        "Content Writing",
        "SEO",
        "Excel",
        "PowerPoint",
    ],
    "leadership": [
        "Scrum",
        "Agile",
        "Project Management",
        "Six Sigma",
    ],
}

# Cluster descriptions (template-based, no LLM)
CLUSTER_DESCRIPTIONS_TEMPLATE = {
    "software_engineering": "Built software engineering systems and applications.",
    "data_engineering": "Built data engineering and data infrastructure systems.",
    "retrieval_ranking": "Built production retrieval, search and ranking systems.",
    "machine_learning": "Built machine learning and statistical modeling systems.",
    "deep_learning": "Worked on deep learning and computer vision systems.",
    "nlp_llm": "Built NLP and LLM-based language intelligence systems.",
    "mlops": "Deployed and monitored machine learning systems in production.",
    "cloud": "Built cloud infrastructure and distributed systems.",
    "database": "Worked with databases and data storage systems.",
    "frontend": "Built frontend and product engineering interfaces.",
    "domain": "Applied domain expertise in business and operations.",
    "leadership": "Led teams and managed projects with process discipline.",
}

CLUSTER_DESCRIPTIONS = {
    "software_engineering": "Experience building software systems and production applications.",
    "data_engineering": "Experience building data pipelines and large-scale data infrastructure.",
    "retrieval_ranking": "Experience with search, retrieval, recommendation and ranking systems.",
    "machine_learning": "Experience applying machine learning models and statistical techniques.",
    "deep_learning": "Experience with deep learning and computer vision systems.",
    "nlp_llm": "Experience with NLP systems, language models and fine-tuning techniques.",
    "mlops": "Experience deploying, serving and monitoring machine learning systems.",
    "cloud": "Experience with cloud infrastructure and distributed systems deployment.",
    "database": "Experience designing and working with database and storage systems.",
    "frontend": "Experience building user interfaces and frontend applications.",
    "domain": "Experience in domain-specific business and industry applications.",
    "leadership": "Experience leading teams, projects and engineering processes.",
}

# Cluster prototypes for semantic matching
CLUSTER_PROTOTYPES = {
    "software_engineering": "software engineering backend frontend api development programming code",
    "data_engineering": "data pipelines etl spark kafka airflow data infrastructure warehouse ingestion",
    "retrieval_ranking": "search retrieval ranking recommendation vector search semantic search matching systems relevance",
    "machine_learning": "machine learning statistical modeling feature engineering forecasting scikit-learn training",
    "deep_learning": "deep learning neural networks computer vision object detection image classification cnn tensorflow",
    "nlp_llm": "nlp natural language processing llm transformers fine-tuning embeddings prompt engineering language",
    "mlops": "mlops model deployment serving monitoring kubeflow mlflow bentoml cicd production pipeline",
    "cloud": "cloud aws azure gcp kubernetes docker terraform infrastructure devops distributed",
    "database": "database sql postgresql mongodb redis data storage query indexing",
    "frontend": "frontend ui ux design angular react figma illustrator photoshop interface",
    "domain": "marketing sales accounting business content writing seo excel operations",
    "leadership": "scrum agile project management six sigma leadership team process",
}

SKILL_TO_CLUSTER = {}
for cluster, skills in SKILL_CLUSTER_MAP.items():
    for skill in skills:
        SKILL_TO_CLUSTER[skill] = cluster


@debug
def cluster_skills(skill_names: list[str]) -> dict[str, list[str]]:
    # Map a list of skill names to cluster buckets.

    clusters = {cluster: [] for cluster in SKILL_CLUSTER_MAP}

    for skill in skill_names:
        cluster = SKILL_TO_CLUSTER.get(skill)
        if cluster:
            clusters[cluster].append(skill)

    # Return while removing empty clusterss
    return {k: v for k, v in clusters.items() if v}


# TODO: ===============Below code generated by LLM, UNCHECKED, CHECK IT=====================


# =============================================================================
# SENTENCE EXTRACTION
# =============================================================================


@debug
def extract_sentences(candidate) -> List[str]:
    """
    Extract clean sentences from candidate profile text.
    Sources: headline, summary, career descriptions.
    """
    sentences = []
    profile = candidate.profile

    # Headline
    headline = profile.headline.strip()
    if headline and len(headline) > 10:
        sentences.append(headline)

    # Summary sentences
    summary = profile.summary.strip()
    if summary:
        for sent in re.split(r"(?<=[.!?])\s+", summary):
            sent = sent.strip()
            if len(sent) > 20 and not sent.startswith("Professional with"):
                sentences.append(sent)

    # Career description sentences
    for career in candidate.career_history:
        desc = career.description.strip()
        if desc:
            for sent in re.split(r"(?<=[.!?])\s+", desc):
                sent = sent.strip()
                if len(sent) > 20:
                    sentences.append(sent)

    # Deduplicate
    seen = set()
    unique = []
    for s in sentences:
        key = s.lower()[:60]
        if key not in seen:
            seen.add(key)
            unique.append(s)

    return unique


# =============================================================================
# EMBEDDING (deterministic, no external APIs)
# =============================================================================


@debug
def _embed(text: str, dim: int = 128) -> np.ndarray:
    """Deterministic word-hash embedding."""
    words = re.findall(r"\b[a-z]+\b", text.lower())
    if not words:
        return np.zeros(dim)

    vectors = []
    for word in words:
        h = hash(word) % (2**31)
        rng = np.random.RandomState(h)
        vectors.append(rng.randn(dim))

    emb = np.mean(vectors, axis=0)
    norm_val = np.linalg.norm(emb)
    if norm_val > 0:
        emb = emb / norm_val
    return emb


@debug
def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


# =============================================================================
# EVIDENCE MATCHING
# =============================================================================


@debug
def find_evidence(sentences: List[str], cluster: str, top_k: int = 3) -> List[str]:
    """
    Find top-k evidence sentences for a cluster using semantic similarity.
    """
    if not sentences:
        return []

    prototype_emb = _embed(CLUSTER_PROTOTYPES.get(cluster, cluster))

    scored = []
    for sent in sentences:
        sent_emb = _embed(sent)
        score = _cosine(sent_emb, prototype_emb)

        # Boost for keyword matches
        lower_sent = sent.lower()
        for kw in CLUSTER_PROTOTYPES.get(cluster, "").split():
            if kw in lower_sent:
                score += 0.15

        scored.append((score, sent))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Deduplicate and return top-k
    result = []
    seen = set()
    for _, sent in scored:
        key = sent.lower()
        if key not in seen:
            seen.add(key)
            result.append(sent)
        if len(result) >= top_k:
            break

    return result


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================


@debug
def cluster_skills_with_evidence(candidate) -> Dict[str, Dict]:
    """
    Cluster candidate skills into domains with description and evidence.

    Args:
        candidate: Candidate object

    Returns:
        {cluster_name: {"description": str, "skills": [str], "evidence": [str]}}
    """
    # Extract all text sentences from candidate
    sentences = extract_sentences(candidate)

    # Cluster skills by domain
    clusters = {cluster: [] for cluster in SKILL_CLUSTER_MAP}
    for skill in candidate.skills:
        name = skill.name
        cluster = SKILL_TO_CLUSTER.get(name)
        if cluster:
            clusters[cluster].append(name)

    # Build result with description + evidence
    result = {}
    for cluster, skills in clusters.items():
        if not skills:
            continue

        evidence = find_evidence(sentences, cluster, top_k=3)
        description = CLUSTER_DESCRIPTIONS_TEMPLATE.get(
            cluster, f"Experience in {cluster}."
        )

        result[cluster] = {
            "description": description,
            "skills": skills,
            "evidence": evidence,
        }

    return result


@debug
def gen_skill_cluster(candidate):
    clusters = defaultdict(list)
    for skill in candidate.skills:
        cluster = SKILL_TO_CLUSTER.get(skill.name)
        if not cluster:
            continue
        clusters[cluster].append(skill)
    return dict(clusters)
