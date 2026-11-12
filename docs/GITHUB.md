# Publish the draft to GitHub

Repository name: **ai-career-forge**

Suggested description (under 350 characters):

> Interactive AI engineering book with deployable portfolio projects. Chapter 1 builds an evidence-based job requirements analyzer using Python, Streamlit, Pydantic, optional structured-output AI, testing, and evaluation. DFW-focused career intelligence is planned.

## Option A — GitHub website

1. Sign in to GitHub and create a repository named `ai-career-forge`.
2. Choose Public if you want a public portfolio and Pages. Review ownership/privacy preferences first.
3. Leave the repository empty: do not add a README, license, or .gitignore because this project includes them.
4. Extract the project ZIP. Upload the **contents of the ai-career-forge folder**, not the ZIP.
5. Browser upload may skip dot-directories. Add `.github/workflows/checks.yml` and `.github/workflows/pages.yml` using GitHub's Create new file feature if missing. Include `.gitignore` and `.streamlit/config.toml` as well.
6. Review the first commit. Verify no secrets or personal documents were added.
7. Open Actions and confirm Python checks pass.

## Option B — PowerShell with GitHub CLI

Open PowerShell in the extracted `ai-career-forge` directory. Confirm `git --version` and `gh --version` work. Authenticate locally with `gh auth login`; never paste tokens into the book or a command saved in Git.

```powershell
git init -b main
git add .
git status --short
git diff --cached --stat
git commit -m "Add Chapter 1 interactive draft and job requirements analyzer"
gh repo create ai-career-forge --public --source=. --remote=origin --push
```

Choose `--private` instead if you prefer. Public Pages availability for private repositories depends on your GitHub plan. If the name already exists, inspect that repository rather than overwriting it. If this folder already contains `.git`, inspect `git status` and `git remote -v` before initializing or adding a remote.

## Option C — Git with a website-created repository

Create the empty repository first. Replace YOUR_GITHUB_USERNAME with your actual account name.

```powershell
git init -b main
git add .
git status --short
git commit -m "Add Chapter 1 interactive draft and analyzer"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ai-career-forge.git
git push -u origin main
```

Git may prompt for GitHub's browser/credential-manager authentication. Do not put a password or access token in the remote URL.

## Later updates

```powershell
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/build_reader.py
git add .
git diff --cached --stat
git commit -m "Improve Chapter 1 lessons and evaluation"
git push
```
