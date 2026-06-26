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
    data: List[Candidate] = load_candidates(candidates_file)

    width = __import__("shutil").get_terminal_size().columns // 2
    bar_width = width - len(f"Checked [] {len(data):,}/{len(data):,}  ")

    total = len(data)

    a = 0
    for i, c in enumerate(data, 1):
        e = c.embed_data
        flag = False

        if len(e["summary"]) > 512:
            flag = True

        for clus in e["skills"]:
            if len(clus) > 512:
                flag = True
                break

        for exp in e["experience"]:
            if len(exp) > 512:
                flag = True
                break

        if flag:
            a += 1

        progress = int(bar_width * i / total)
        print(
            f"Checked [{'#' * progress + ' ' * (bar_width - progress)}] {i:07,}/{total:,}  ",
            end="\r",
        )

    print()
    print(f"{a:,} people have their embedding data going beyond 512 tokens")


if __name__ == "__main__":
    main(
        **parse_args(
            candidates_file="candidates.jsonl",
            output_path="submission.csv",
        )
    )
