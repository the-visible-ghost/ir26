# Phantom Devs - India Runs 2026
## Important CRITICAL Note:
> ### This repository uses Git Large File Storage (Git LFS).

<br>

# Setup Instructions
> **NOTE:** All Paths are POXIS-style paths (delimited by `/`)\
that will work in Linux and BSD based Operating Systems.

> **In Windows:** Use `\\` as delimiter in paths.

## 1. <ins>CRITICAL</ins> - Installing REQUIRED dependency: git-lfs
### 1.1 Installing **[Git LFS](https://git-lfs.com/)**

You can install **[Git LFS](https://git-lfs.com/)** by visiting the **[Official Website](https://git-lfs.com/)**.\
Or by running example commands for your specific operating system given below.

#### On Arch based OS (Arch, Manjaro, Garuda, EndeavourOS, Omarchy, Artix, etc)
- _You can use your favorite AUR helpers like: **`yay`**, **`paru`**, etc_
- `sudo pacman -S --noconfirm git-lfs`

#### On Debian based OS (Debian, Ubuntu, Mint, Kali, etc)
- `sudo apt install -y git-lfs`

#### On Fedora based OS (Fedora, Nobara, etc)
- `sudo dnf install -y git-lfs`

#### Other Operating Systems -
- Visit Git LFS **[Official Website Here](https://git-lfs.com/)** for instructions.

### 1.2 Setup Git LFS with your user account
```bash
git lfs install
```

## 2. Cloning the Repository
Clone the repository using the command below.
> ### _**Make sure you have Git LFS installed and setted up properly before this**_
```bash
git clone https://github.com/the-visible-ghost/India-Runs-2026.git
```
Change current working directory to the repository root using the command below.
```bash
cd India-Runs-2026
```

## 3. Creating a virtual environment.

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
## 6. Verifying installation
Run the command below to verify if the setup/installation is successful and valid.
```bash
python verify_installation.py
```
The command must display **`Ready to Rank`** after performing necessary checks.

<br>

# Running the ranker
```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

<br>
