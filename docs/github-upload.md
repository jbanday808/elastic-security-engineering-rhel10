# Create and Publish the Lab Repository with WSL + VS Code

Use this guide to prepare the project in Ubuntu on WSL, review its contents, and publish it to GitHub. The local folder is `~/projects/rhel10-elastic-security-deployment`; the GitHub repository name is `elastic-security-engineering-rhel10`.

## 1. Verify WSL and Ubuntu

Open Windows PowerShell and check the WSL installation and available distributions:

```powershell
wsl --status
wsl -l -v
```

If Ubuntu is not installed, run:

```powershell
wsl --install -d Ubuntu
```

Complete any required restart and Ubuntu account setup before continuing.

## 2. Install VS Code and Required Packages

Install Visual Studio Code on Windows and add Microsoft's official **WSL** extension. Open Ubuntu and install the required packages:

```bash
sudo apt update
sudo apt install -y git unzip tree
```

## 3. Extract and Open the Project

Download the prepared ZIP file and make it accessible from Ubuntu. Create the parent directory:

```bash
mkdir -p ~/projects
```

Extract the archive into that directory, replacing the example archive path with its actual location:

```bash
unzip /path/to/prepared-project.zip -d ~/projects
```

Confirm that the extracted project folder is named `rhel10-elastic-security-deployment`. Avoid extracting over an existing working copy. Open the project in VS Code:

```bash
cd ~/projects/rhel10-elastic-security-deployment
code .
```

Confirm that VS Code is connected to Ubuntu through WSL.

## 4. Verify the Screenshots

From the project root, run the screenshot inventory check:

```bash
bash scripts/verify-screenshots.sh
```

Resolve any missing figures before publishing. After initializing Git in Section 7, check the working tree with:

```bash
git status --short
```

## 5. Review Files for Sensitive Information

Review every file and screenshot before staging it. Check for:

- Passwords, API keys, and client secrets.
- Fleet enrollment tokens and credential-bearing installation commands.
- Confidential configuration values and unredacted lab notes.
- Hostnames, IP addresses, usernames, and other identifiers that should remain private.

Follow the [security publication checklist](security-publication-checklist.md). Git ignore rules do not remove sensitive content from files already tracked by Git.

## 6. Configure Your Git Identity

Replace the placeholders with your name and verified GitHub email address:

```bash
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR VERIFIED GITHUB EMAIL"
```

These settings apply to all repositories for your Ubuntu user. Omit the global option and configure them after initialization if you want an identity specific to this repository.

## 7. Initialize Git and Stage Approved Files

For a new local repository, initialize the main branch:

```bash
git init -b main
```

Stage the following paths only after reviewing their contents:

```bash
git add README.md .gitignore .gitattributes .vscode docs assets examples queries scripts
```

Review the working tree:

```bash
git status --short
```

## 8. Review and Commit the Staged Changes

Inspect the staged file summary and full text changes:

```bash
git diff --cached --stat
git diff --cached
```

Review staged images separately; a text diff does not display their contents. Once the staged changes are approved, create the initial commit:

```bash
git commit -m "Document RHEL 10 Elastic Security home lab"
```

## 9. Choose a GitHub Connection Method

Choose one of the following workflows.

**GitHub CLI:** If the CLI is installed, authenticate from Ubuntu:

```bash
gh auth login
```

Follow the prompts to connect your GitHub account. If the CLI is unavailable, use the manual workflow below.

**GitHub website:** Create a private repository named `elastic-security-engineering-rhel10` on GitHub. Leave the initial README, `.gitignore`, and license options unselected so the remote repository is empty. Connect the local repository, replacing the username placeholder:

```bash
git remote add origin https://github.com/YOUR-USERNAME/elastic-security-engineering-rhel10.git
```

Adding a remote does not authenticate you. Use your configured GitHub HTTPS authentication method when pushing; do not embed credentials in the remote URL.

## 10. Publish the Repository

If you created an empty repository on the GitHub website and added its remote in Section 9, push the local main branch:

```bash
git push -u origin main
```

Alternatively, if the GitHub repository does not yet exist and you authenticated through GitHub CLI, create and publish a private repository:

```bash
gh repo create elastic-security-engineering-rhel10 --private --source=. --remote=origin --push
```

Use only the workflow that matches your setup. If an existing remote repository already contains an initial README, `.gitignore`, license, or other commits, review and reconcile its history before pushing. Do not overwrite it with a force push.

## 11. Verify the Published Repository

Open the repository on GitHub and confirm that:

- The README and documentation render correctly.
- Architecture and screenshot links display the intended images.
- Queries, examples, and scripts are present.
- No sensitive information was included.

Keep the repository private until the final review is complete. If you choose to publish it publicly, change its visibility through the repository settings after reviewing the disclosure implications.

## Important Note

The original `.docx` lab notes are intentionally excluded because they may contain authentication credentials or enrollment secrets. Do not add unredacted copies to the repository. Rotate any exposed credentials that are still active; deleting a file does not invalidate its secrets or remove them from Git history.
