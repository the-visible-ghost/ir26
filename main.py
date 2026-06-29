from typing import List
from utils import debug, parse_args, path
from utils.candidate import Candidate


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
def main(candidates_file: str, output_path: str):
    data = load_candidates(candidates_file)
    print(data[0].candidate_id)


if __name__ == "__main__":
    main(
        **parse_args(
            candidates_file="candidates.jsonl",
            output_path="submission.csv",
        )
    )
