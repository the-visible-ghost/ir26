OUTPUT_PATH = "./submission.csv"
CANDIDATES_FILE = "./candidates.jsonl"
IS_GZIPPED = False


def main():
    from csv import writer as csv_writer

    print(f"{OUTPUT_PATH = }", f"{CANDIDATES_FILE = }", f"{IS_GZIPPED = }", sep="\n")


if __name__ == "__main__":
    import sys

    if "--help" in sys.argv:
        print(
            "\nUSAGE: python rank.py [OPTIONS]\n",
            "OPTIONS:",
            "   --help                  Displays this message.\n",
            "   --out [NAME]            Name of the output CSV file.",
            "                           Defaults to " + OUTPUT_PATH + "\n",
            "   --candidates [FILE]     The JSON (optionally g-zipped) file that contains a list of candidates",
            "                           Defaults to " + CANDIDATES_FILE + "\n",
            "   --gzipped               Use ONLY if the candidates files is gzipped and needs inline de-compression",
            "                           Default to " + str(IS_GZIPPED) + "\n",
            sep="\n",
        )
        exit(0)

    if "--out" in sys.argv:
        _out_arg_index = sys.argv.index("--out")
        if len(sys.argv) <= _out_arg_index + 1:
            raise RuntimeError(
                "No file specified after --out, see python rank.py --help"
            )
        out_name = sys.argv[_out_arg_index + 1]
        if "." in out_name and out_name.rsplit(".")[-1].lower() != "csv":
            raise RuntimeError("Output file must be a CSV file")
        OUTPUT_PATH = out_name

    if "--candidates" in sys.argv:
        _candi_arg_index = sys.argv.index("--candidates")
        if len(sys.argv) <= _candi_arg_index + 1:
            raise RuntimeError(
                "No file specified after --candidates, see python rank.py --help"
            )
        CANDIDATES_FILE = sys.argv[_candi_arg_index + 1]

    if "--gzipped" in sys.argv:
        IS_GZIPPED = True

    main()
