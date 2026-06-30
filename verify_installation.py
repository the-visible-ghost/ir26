"""
this code: Verifies that the environment is correctly configured to run rank.py.

Checks:
- Python version
- Required Python modules
- Repository files
- Processed data files
- FAISS index readability
- Git LFS installation
- Git LFS tracked files downloaded correctly

If everything is valid, prints:
    Ready to Rank
"""

from __future__ import annotations

import importlib
import shutil
import subprocess
import sys
from pathlib import Path

# -------------------------------------------------------------

ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "requirements.txt",
    "main.py",
    "rank.py",
]

PROCESSED_FILES = [
    "processed/job_desc.json",
    "processed/summary_lookup.json",
    "processed/skills_lookup.json",
    "processed/experience_lookup.json",
    "processed/summary_index.faiss",
    "processed/skills_index.faiss",
    "processed/experience_index.faiss",
]

REQUIRED_MODULES = {
    "numpy": "numpy",
    "faiss": "faiss-cpu / faiss",
    "msgspec": "msgspec",
}

# -------------------------------------------------------------


class Colors:
    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    CYAN: str = "\033[96m"
    BOLD: str = "\033[1m"
    RESET: str = "\033[0m"


def supports_color():
    return sys.stdout.isatty()


if not supports_color():
    Colors.RED = ""
    Colors.GREEN = ""
    Colors.YELLOW = ""
    Colors.CYAN = ""
    Colors.BOLD = ""
    Colors.RESET = ""


def header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")


def ok(text):
    print(f"{Colors.GREEN}✔{Colors.RESET} {text}")


def warn(text):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def fail(text):
    print(f"{Colors.RED}✖{Colors.RESET} {text}")


def separator():
    print("-" * 60)


# -------------------------------------------------------------

errors = []


def add_error(msg):
    errors.append(msg)
    fail(msg)


# -------------------------------------------------------------
# Python version
# -------------------------------------------------------------

header("Python")

if sys.version_info >= (3, 9):
    ok(
        f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
else:
    add_error(
        f"Python >= 3.9 required (found {sys.version_info.major}.{sys.version_info.minor})"
    )


# -------------------------------------------------------------
# Git LFS
# -------------------------------------------------------------

header("Git LFS")

git_lfs_available = False

if shutil.which("git") is None:
    add_error("Git is not installed.")
else:
    ok("Git found.")

    if shutil.which("git-lfs") is None:
        add_error("Git LFS is not installed.")
    else:
        git_lfs_available = True
        ok("Git LFS found.")

        try:
            subprocess.run(
                ["git", "lfs", "env"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
            ok("Git LFS initialized.")
        except Exception:
            add_error(
                "Git LFS appears to be installed but not initialized. Run:\n    git lfs install"
            )

# -------------------------------------------------------------
# Python packages
# -------------------------------------------------------------

header("Python Packages")

for module, package in REQUIRED_MODULES.items():
    try:
        importlib.import_module(module)
        ok(module)
    except Exception as e:
        add_error(f"Cannot import '{module}' ({package}) : {e}")

# -------------------------------------------------------------
# Repository files
# -------------------------------------------------------------

header("Repository Files")

for file in REQUIRED_FILES:
    p = ROOT / file
    if p.exists():
        ok(file)
    else:
        add_error(f"Missing file: {file}")

# -------------------------------------------------------------
# Processed data
# -------------------------------------------------------------

header("Processed Files")

LFS_POINTER_SIGNATURE = b"version https://git-lfs.github.com/spec/v1"

for file in PROCESSED_FILES:
    p = ROOT / file

    if not p.exists():
        add_error(f"Missing file: {file}")
        continue

    if p.stat().st_size == 0:
        add_error(f"Empty file: {file}")
        continue

    try:
        with open(p, "rb") as fp:
            head = fp.read(256)

        if head.startswith(LFS_POINTER_SIGNATURE):
            add_error(f"{file} is still a Git LFS pointer.\nRun:\n    git lfs pull")
            continue

    except Exception as e:
        add_error(f"Unable to read {file}: {e}")
        continue

    ok(file)

# -------------------------------------------------------------
# FAISS index validation
# -------------------------------------------------------------

header("FAISS Index Validation")

try:
    import faiss

    for file in [
        "processed/summary_index.faiss",
        "processed/skills_index.faiss",
        "processed/experience_index.faiss",
    ]:
        p = ROOT / file

        if not p.exists():
            continue

        try:
            index = faiss.read_index(str(p))
            ok(f"{file} ({index.ntotal} vectors)")
        except Exception as e:
            add_error(f"Cannot load {file}: {e}")

except Exception:
    warn("Skipping FAISS validation (faiss import failed).")

# -------------------------------------------------------------
# Final
# -------------------------------------------------------------

separator()

if errors:
    print(
        f"\n{Colors.BOLD}{Colors.RED}"
        f"Verification Failed ({len(errors)} issue{'s' if len(errors) != 1 else ''})"
        f"{Colors.RESET}\n"
    )

    print("Please resolve the above issue(s) and run:")
    print("    python verify_installation.py\n")

    sys.exit(1)

print(
    f"""
{Colors.GREEN}{Colors.BOLD}
============================================================
                     Ready to Rank
============================================================
{Colors.RESET}
"""
)
sys.exit(0)
