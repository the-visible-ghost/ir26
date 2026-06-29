import utils
import faiss
import numpy as np

from typing import Dict, List
from utils import (
    debug,
    parse_args,
    path,
    load_json_file,
)
from utils.candidate import Candidate
from utils.embedding import Embedder


@debug
def load_candidates(file: str) -> List[Candidate]:
    decode = __import__("msgspec").json.decode
    with (
        __import__("gzip").open(file, "rb")
        if path.basename(file).endswith(".gz")
        else open(file, "rb")
    ) as fp:
        return [decode(line, type=Candidate) for line in fp]


@debug
def load_job_desc(file: str) -> Dict[str, np.ndarray]:
    with open(file, "r") as fp:
        return {
            section: np.array(vectors)
            for section, vectors in __import__("json").load(fp).items()
        }


@debug
def main(candidates_file: str, output_path: str):
    embedder = Embedder(
        name="BAAI/bge-base-en-v1.5",
        path="./models/bge-bage-en-v1.5",
    )

    candidates: List[Candidate] = load_candidates(candidates_file)

    job_desc = load_job_desc("./processed/job_desc.json")

    summary_lookup = load_json_file("./processed/summary_lookup.json")
    skills_lookup = load_json_file("./processed/skills_lookup.json")
    experience_lookup = load_json_file("./processed/experience_lookup.json")

    summary_index = faiss.read_index("./processed/summary_index.faiss")
    skills_index = faiss.read_index("./processed/skills_index.faiss")
    experience_index = faiss.read_index("./processed/experience_index.faiss")


if __name__ == "__main__":
    main(
        **parse_args(
            candidates_file="candidates.jsonl",
            output_path="submission.csv",
        )
    )
