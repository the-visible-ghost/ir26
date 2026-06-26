from typing import List
from utils import debug, parse_args, path
from utils.candidate import Candidate


@debug
def load_candidates(file) -> List[Candidate]:
    decode = __import__("msgspec").json.decode
    with (
        __import__("gzip").open(file, "rb")
        if path.basename(file).endswith(".gz")
        else open(file, "rb")
    ) as fp:
        return [decode(line, type=Candidate) for line in fp]


@debug
def main(candidates_file, output_path):
    data = load_candidates(candidates_file)


if __name__ == "__main__":
    main(
        **parse_args(
            candidates_file="candidates.jsonl",
            output_path="submission.csv",
        )
    )
