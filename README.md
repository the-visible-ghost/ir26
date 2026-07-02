# PhantomDevs - India Runs 2026

<br>

# Setup Instructions
> **NOTE:** All Paths are POXIS-style paths (delimited by `/`)\
that will work in Linux and BSD based Operating Systems.

> **In Windows:** Use `\\` as delimiter in paths.

## 1. Cloning the Repository
Clone the repository using the command below.
```bash
git clone https://github.com/the-visible-ghost/ir26.git
```
Change current working directory to the repository root using the command below.
```bash
cd ir26
```

## 2. Creating a virtual environment.

> ### _**If you DON'T already have a .venv (python virtual environment)**_

Create a Python Virtual Environment using the command below -
```bash
python -m venv .venv
```

## 4. Activate the virtual environment
Source **`activate.bat`** or **`activate.fish`** or **`activate.zsh`** etc file based on your shell.
```bash
source .venv/bin/activate
```

## 5. Installing dependencies
Run the command below to install required dependencies
```bash
pip install -r requirements.txt
```

<br>

# Running the ranker
```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

<br>
