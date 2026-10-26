# Security review before GitHub publication

**STOP: Review and rotate any real credentials present in your original notes or screenshots before publishing a public repository.** The original RHEL deployment document contains plaintext login/enrollment and cloud-application credentials, so its unedited copy must not be committed.

- [ ] Revoke/rotate any exposed Elastic enrollment tokens and Azure application client secrets.
- [ ] Remove passwords, keys, OAuth tokens, service-account files, and connection strings from every file.
- [ ] Review screenshots for secrets, customer identities, and information you do not want public.
- [ ] Keep real configurations containing private values outside this repository.
- [ ] Use only the sanitized example files under `examples/`.
- [ ] Run `git status --short`, `git diff --cached --stat`, and `git diff --cached` before committing.
- [ ] Prefer staged file paths rather than `git add .` until everything has been checked.
- [ ] Do not publish the original `.docx` files until they have been individually reviewed and redacted (including images, headers, comments, and metadata).
- [ ] Use GitHub private visibility first if you are unsure; make it public after verification.

Do not assume `.gitignore` protects files already committed. If a secret has been committed, revoke or rotate it promptly and follow GitHub's removal guidance.
