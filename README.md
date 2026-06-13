# Phantom Devs - India Runs 2026

# Setup Instructions
> **NOTE:** All Paths are POXIS-style paths (delimited by `/`) that will work in Linux and MacOS\
**In Windows:** Use `\\` as delimiter in paths

## 1. Creating a virtual environment.

### _If you DON'T already have a .venv (python virtual environment)_
Create a Python Virtual Environment using the command below -
```bash
python -m venv .venv
```
## 2. Activate the virtual environment
Source `.bat` or `.fish` or `.zsh` etc file based on your shell.
```bash
source .venv/bin/activate
```

## 2. Installing dependencies
```bash
pip install -r requirements.txt
```
<br>

# Running the ranker
```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

