from os import path
from sys import argv
from time import perf_counter
from typing import Dict, Literal


def show_help(candidates_file, output_path):
    print(
        "\nUSAGE: python " + path.basename(argv[0]) + " [OPTIONS]\n",
        "OPTIONS:",
        "   --help                  Displays this message.\n",
        "   --candidates <FILE>     The JSON [optionally g-zipped] file that contains a list of candidates",
        '                           MUST end with a ".jsonl" or ".jsonl.gz" file extension',
        '                           Defaults to "' + candidates_file + '"\n',
        '   --out <NAME>            Name of the output CSV file. [MUST end with a ".csv" file extension]',
        '                           Defaults to "' + output_path + '"\n',
        "   --debug                 Enable debug mode (verbose logging)",
        sep="\n",
    )


def debug_print(*args, **kwargs):
    if "--debug" in argv:
        print("[DEBUG]:", *args, **kwargs)


def debug(func):
    def wrapper(*args, **kwargs):
        debug_print(f"{func.__qualname__}({'...' if args or kwargs else ''}) called")
        start = perf_counter()
        retval = func(*args, **kwargs)
        elapsed = perf_counter() - start
        debug_print(
            f"{func.__qualname__}({'...' if args or kwargs else ''}) "
            f"{'finished' if retval is None else 'returned'} in {elapsed:.3f} s"
        )
        return retval

    return wrapper


@debug
def parse_args(
    *, candidates_file: str, output_path: str
) -> Dict[Literal["candidates_file", "output_path"], str]:
    import sys

    if "--help" in sys.argv:
        show_help(candidates_file, output_path)
        exit(0)

    if "--out" in sys.argv:
        _out_arg_index = sys.argv.index("--out")
        if len(sys.argv) <= _out_arg_index + 1:
            sys.tracebacklimit = 0
            print()
            raise RuntimeError(
                "No file specified after --out, "
                f"see python {path.basename(argv[0])} --help"
            )
        if not path.basename(sys.argv[_out_arg_index + 1]).endswith(".csv"):
            sys.tracebacklimit = 0
            print()
            raise RuntimeError("Output file must be a CSV file")
        output_path = sys.argv[_out_arg_index + 1]

    if "--candidates" in sys.argv:
        _candi_arg_index = sys.argv.index("--candidates")
        if len(sys.argv) <= _candi_arg_index + 1:
            sys.tracebacklimit = 0
            print()
            raise EOFError(
                "No file specified after --candidates, "
                f"see python {path.basename(argv[0])} --help"
            )
        candi_name = path.basename(sys.argv[_candi_arg_index + 1])
        if not (candi_name.endswith(".jsonl") or candi_name.endswith(".jsonl.gz")):
            sys.tracebacklimit = 0
            print()
            raise RuntimeError("Candidates file must be a .jsonl or .jsonl.gz")
        candidates_file = sys.argv[_candi_arg_index + 1]

    if not (path.exists(candidates_file) and path.isfile(candidates_file)):
        sys.tracebacklimit = 0
        print()
        raise FileNotFoundError(
            f'ERROR: Candidates file not found: "{candidates_file}"\n\n'
            f"For more info run:  python {path.basename(argv[0])} --help"
        )

    sys.tracebacklimit = None

    return {
        "candidates_file": candidates_file,
        "output_path": output_path,
    }


from . import candidate, embedding, job_desc

__all__ = (
    "candidate",
    "embedding",
    "job_desc",
)
