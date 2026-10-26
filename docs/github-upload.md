# Create and publish the lab repository with WSL + VS Code

1. In Windows PowerShell run `wsl --status` and `wsl -l -v`; install Ubuntu if needed with `wsl --install -d Ubuntu`.
2. Install VS Code (Windows) and the official WSL extension. In Ubuntu: `sudo apt update && sudo apt install -y git unzip tree`.
3. Download the prepared ZIP, copy it into your Ubuntu home directory or work from `~/projects`, unzip it into `~/projects`, then run `cd ~/projects/elastic-security-rhel10-home-lab && code .`.
4. Run `bash scripts/verify-screenshots.sh`, followed by `git status --short` after initialization.
5. Review every file and image for secrets, especially any unredacted original documentation that you might add later. See the security checklist.
6. Set Git identity: `git config --global user.name "YOUR NAME"` and `git config --global user.email "YOUR VERIFIED GITHUB EMAIL"`.
7. `git init -b main`; stage only the approved public files: `git add README.md .gitignore .gitattributes .vscode docs assets examples queries scripts`.
8. Review `git diff --cached --stat` and `git diff --cached`, then `git commit -m "Document RHEL 10 Elastic Security home lab"`.
9. Sign in through GitHub CLI (`gh auth login`) or create an empty repo on github.com and connect with `git remote add origin https://github.com/YOUR-USERNAME/elastic-security-rhel10-home-lab.git`.
10. If you created the repo in the GitHub website (without initial README/.gitignore/license), run `git push -u origin main`. Otherwise `gh repo create elastic-security-rhel10-home-lab --private --source=. --remote=origin --push`.
11. Confirm files and screenshots appear in GitHub. After another review, optionally switch repository visibility from Private to Public.

The original `.docx` lab notes are intentionally excluded because they contain authentication and enrollment secrets. Rotate exposed credentials if still active.
