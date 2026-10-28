# RHEL 10 STIG/SCAP integration task plan

Target: https://github.com/jbanday808/elastic-security-engineering-rhel10

Status: proposed implementation backlog; no host changes or validation performed. Repository access returned HTTP 403, and connected GitHub read tools were unavailable. The source guide, current repository paths, versions, and existing tests could not be inspected. This draft preserves the supplied installation → configuration → deployment → validation sequence; Task 01 must establish exact guide traceability before implementation. Paths and task entry points below are proposals, not existing commands.

## Highest-risk validation gaps to resolve first

These are unverified risks to investigate, not findings against the repository.

| Priority | Question and release gate | Tasks |
|---|---|---|
| P0 | Does the installed content actually contain a RHEL 10 STIG profile for the target release? A filename, successful package install, or another RHEL version's profile is insufficient. Block remediation until provenance, profile ID, applicability, and benchmark revision are recorded. | 01–03 |
| P0 | Can the host recover after changes to authentication, audit, firewall, cryptography, or boot settings? Prove console access and snapshot restoration before applying changes. | 02, 05–06 |
| P0 | Does hardening preserve Elastic telemetry and host access after reboot? Require a fresh post-reboot event in Elastic, not merely an active service. | 04, 06–07 |
| P1 | Can scan execution failure be distinguished from noncompliance? Preserve OpenSCAP exit codes; reject missing, malformed, wrong-host, stale, or incomplete results. | 03, 07 |
| P1 | Are exceptions and manual checks explicit? Track failed, error, unknown, notchecked, notapplicable, and excluded rules separately; do not equate a high score with STIG compliance. | 05, 07 |
| P1 | Are duplicate/retried results, content changes, and sensitive evidence handled consistently? Require stable identity, content hashes, restricted evidence, and repeatable ingestion. | 04, 08 |

## Execution and evidence contract

Implement each task as a separate reviewable change. Execute host-changing tasks only on a disposable RHEL 10 canary until the final gate passes. Use the guide's actual Elastic deployment model; do not assume Fleet-managed versus standalone Agent, or that SCAP ingestion already exists.

Proposed repository deliverables:

```text
docs/rhel10-stig-scap-task-plan.md
docs/rhel10-stig-scap-source-map.md
config/scap/manifest.yaml
config/scap/tailoring.xml
scripts/scap/{preflight,install,baseline,generate,apply,validate}.sh
scripts/scap/normalize.py
tests/scap/fixtures/
tests/scap/test_results.py
```

Choose the repository's existing task runner during Task 01. Suggested target contract: `scap-preflight`, `scap-install`, `scap-baseline`, `scap-generate`, `scap-apply`, `scap-validate`. These targets must be implemented before use. Read-only operations must never invoke remediation; apply must require an explicit canary/change identifier and a verified recovery checkpoint. CI must not run privileged remediation on shared runners.

Each run records UTC start/end, host identity, RHEL release, repository commit, package versions, datastream/tailoring hashes, selected profile, benchmark revision, command arguments with secrets removed, exit status, and operator/change ID. Store raw evidence outside Git under access controls and retention rules; commit only sanitized fixtures and evidence references. Raw ARF/XML, HTML, logs, and configuration backups may expose host details. Hash the final evidence bundle and record its restricted location.

## Ordered tasks

### 01 — Map the guide to repository tasks and freeze inputs

**Prerequisites:** A readable checkout of the repository and its actual RHEL 10 STIG/SCAP guide.

**Work and commands:** Read repository instructions first. Run `git rev-parse HEAD`, `git status --short`, and `rg -n -i 'rhel.?10|stig|scap|oscap|remediat|elastic.agent' .`. Map every installation, configuration, deployment, and validation section to a task below. Record existing scripts and tests rather than duplicating them. Define the supported RHEL minor release, architecture, Elastic versions, deployment mode, source benchmark revision, expected services, and evidence location in the manifest.

**Expected result / acceptance:** Every guide step has a source path/section, task ID, command, and verification method. Unknown versions and unsupported combinations are explicit blockers. Exact existing repository commands replace draft placeholders. No RHEL 9 content is silently substituted.

**Rollback point:** Documentation-only diff; discard or revert that isolated change.

**Evidence:** Guide source map, commit SHA, version manifest, and unresolved compatibility decisions.

### 02 — Implement preflight and prove recovery

**Prerequisites:** Task 01; disposable RHEL 10 canary, approved repositories, sudo, console access, and a platform snapshot/restore procedure.

**Work and commands:** Implement the preflight wrapper using `cat /etc/redhat-release`, `uname -m`, `id`, `df -h`, `timedatectl status`, `getenforce`, `systemctl --failed`, and `sudo dnf repolist`. Record routing/DNS and the required Elastic destinations without exposing credentials. Capture the currently configured authentication, audit, firewall, crypto, and Agent state with commands appropriate to installed services. Take a platform snapshot and restore it once before proceeding; record the exact platform commands in the runbook. Verify a fresh administrative login and console recovery.

**Expected result / acceptance:** Preflight rejects the wrong OS, missing privilege, insufficient capacity, unavailable content sources, and missing recovery reference. Snapshot restoration has been demonstrated, with a recorded recovery duration and a working login. Do not claim a configuration backup alone can reverse boot or filesystem changes.

**Rollback point:** Restored clean snapshot. Stop if recovery cannot be demonstrated.

**Evidence:** Sanitized inventory, dependency results, snapshot ID, restore transcript, and access checks.

### 03 — Install OpenSCAP and validate content before a baseline scan

**Prerequisites:** Task 02; manifest specifies approved package/content sources.

**Work and commands:** On the canary, run:

```bash
sudo dnf install -y openscap-scanner scap-security-guide
rpm -q openscap-scanner scap-security-guide
oscap --version
rpm -ql scap-security-guide
```

Discover the actual RHEL 10 datastream from the package listing. Set `DATASTREAM` to that reviewed absolute path and `PROFILE` to the full ID shown by `oscap info "$DATASTREAM"`. Run `oscap ds sds-validate "$DATASTREAM"` and `sha256sum "$DATASTREAM"`. If RHEL 10 STIG content is absent, stop and resolve an approved content source; do not invent a profile ID or infer official STIG coverage from generic content.

Set `RUN_DIR` to a new, restricted absolute evidence directory and run this command in a wrapper that records the return status even when the evaluator returns nonzero:

```bash
sudo oscap xccdf eval --profile "$PROFILE" \
  --results-arf "$RUN_DIR/baseline.arf.xml" \
  --report "$RUN_DIR/baseline.html" "$DATASTREAM"
```

**Expected result / acceptance:** Content is valid, hash-pinned, and applicable to RHEL 10; the selected profile and benchmark provenance are recorded. A completed baseline has nonzero evaluated rule count and correct host/time metadata. Treat exit 0 as evaluation without failures, exit 2 as evaluation with failing rules, and other codes as execution errors, confirming behavior against the installed OpenSCAP documentation. A completed scan with failing rules is usable evidence, not a deployment approval.

**Rollback point:** Restore the pre-install snapshot if package changes must be reversed; retain baseline evidence. The scan must not use `--remediate`.

**Evidence:** Package versions, `oscap info`, validation output/status, content checksum, baseline ARF, HTML, evaluator logs, and rule-status counts.

### 04 — Configure the Elastic integration and prove baseline delivery

**Prerequisites:** Task 03; actual Agent deployment mode and approved output/CA configuration identified in Task 01.

**Work and commands:** Follow the source guide's Agent installation/enrollment commands through a secret-safe deployment wrapper; do not commit tokens. Use `sudo elastic-agent status` where the installed binary supports it and inspect the installed Agent service with `systemctl`. Validate TLS using the configured CA; do not bypass verification. Define the SCAP path separately from ordinary audit/system telemetry: normalize completed ARF results into a documented JSON schema and ship through the project's supported integration or pipeline.

The normalized contract must retain host identity, scan/run ID, scan timestamps, benchmark/profile/version, content hash, rule ID, severity, and the original XCCDF result. Define stable per-scan/per-rule event identity and index/data-stream names. Validate against fixtures before configuring mappings. Publish one baseline scan and search the chosen destination for that exact host and run ID; document the concrete API or Kibana query after discovering the actual schema.

**Expected result / acceptance:** Required ordinary host telemetry and baseline SCAP records are searchable with correct types, timestamps, rule counts, and no parser failures. Successful Agent enrollment alone does not pass. A deliberate malformed input is rejected or quarantined visibly; retrying an identical scan follows the documented deduplication policy.

**Rollback point:** Restore the previous Agent policy/output and versioned pipeline/mapping configuration. Use an isolated test destination so rollback does not delete shared evidence.

**Evidence:** Redacted policy, mapping/pipeline versions, fixture results, Agent status, delivery latency, exact query, and returned sample/count reconciliation.

### 05 — Configure tailoring and review remediation before deployment

**Prerequisites:** Tasks 03–04; baseline triage and access to the benchmark's manual requirements.

**Work and commands:** Classify each failed or unevaluated rule as automated remediation, manual action, investigation, or a proposed exception. For every exception record rule ID, rationale, owner, approval, expiry, and compensating control. Create and validate tailoring using the installed OpenSCAP-supported workflow; record the effective tailored profile and hash. Generate a fix from the specific baseline result:

```bash
oscap xccdf generate fix --fix-type bash \
  --result-id "$RESULT_ID" \
  --output "$RUN_DIR/remediation.sh" "$RUN_DIR/baseline.arf.xml"
bash -n "$RUN_DIR/remediation.sh"
```

Discover `RESULT_ID` from the actual evaluation document. If that OpenSCAP build requires extracted XCCDF input, document and validate the supported extraction step first. An untailored baseline must be rerun with tailoring before generating the tailored fix. Review every generated action for authentication, audit ownership/conflicts, firewall reachability, crypto/TLS, filesystem/boot effects, and Elastic compatibility. Generate a separate reviewed procedure for rules without an automatic fix.

**Expected result / acceptance:** Every actionable finding has a disposition. Generated changes match the selected result/profile and are reviewed; no unreviewed blanket remediation is runnable. Tailoring exclusions are visible in reports. Any audit collector ownership conflict has a supported resolution.

**Rollback point:** Versioned manifest/tailoring and untouched pre-hardening canary. Generation must not apply changes.

**Evidence:** Rule disposition register, tailoring/hash, exact result ID, fix checksum, syntax-check result, and review/change record.

### 06 — Deploy reviewed remediation to the canary and reboot

**Prerequisites:** Task 05; fresh pre-change snapshot, tested console access, approved change window, and unchanged content/fix hashes.

**Work and commands:** The apply wrapper verifies the canary identity, recovery reference, reviewed fix checksum, and approved rule dispositions before running `sudo bash "$RUN_DIR/remediation.sh"`. Record status and restricted logs; halt on a partial or failed run. Execute documented manual changes separately. Reboot through the approved host/platform procedure when required. After reconnecting, check `systemctl --failed`, a fresh administrative login, expected network access, SELinux mode, Agent health, and the guide's workload service checks.

**Expected result / acceptance:** The host boots, administration works, expected services and TLS connectivity pass, and a fresh post-reboot host event appears in Elastic. Any access loss, failed required service, unexplained change, or telemetry interruption triggers rollback and blocks rollout.

**Rollback point:** Restore the pre-change snapshot and previous external Agent policy/pipeline versions as applicable; verify host access and telemetry again. Restoring the VM does not undo changes made in Elastic.

**Evidence:** Change transcript/status, snapshot reference, boot time, service/login results, Agent status, post-reboot event ID/timestamp, and any restore outcome.

### 07 — Validate post-hardening results and reconcile Elastic evidence

**Prerequisites:** Successful Task 06; same pinned datastream and effective tailoring as the approved baseline.

**Work and commands:** Repeat Task 03's evaluation into distinct `post.arf.xml` and `post.html` files, adding the reviewed tailoring arguments when applicable. Compare results by rule ID and status, not score alone. Reconcile raw scan counts against normalized and indexed counts using the run ID. Validate authentication, audit event delivery, workload behavior, and required TLS connections. Resolve manual checks through separate evidence and reviewer disposition.

**Expected result / acceptance:** No unexpected regression; targeted remediations pass or have a documented investigation. No unexplained error, unknown, notchecked, missing rule, or change in applicability is accepted. All remaining failures/exclusions have approved, current dispositions; manual checks have evidence. Elastic rule counts match the source under the documented event model, and a fresh post-hardening event satisfies the delivery window defined in Task 01. Report automated coverage and residual risk explicitly; do not label the host STIG compliant from a scan score alone.

**Rollback point:** Task 06 checkpoint for regressions caused by hardening; retain failed validation evidence. Fix ingestion independently if the raw scan is valid but delivery fails.

**Evidence:** Post-scan ARF/HTML/logs/status, per-rule before/after diff, manual checklist, exception register, source-to-index reconciliation, and service/telemetry checks.

### 08 — Add regression gates and stage the rollout

**Prerequisites:** Task 07 accepted; recovery and evidence procedures complete.

**Work and commands:** Implement `tests/scap/test_results.py` and sanitized fixtures for passing/failing rules, evaluator errors, empty/truncated input, wrong profile/host, stale scans, exclusions, and duplicate delivery. Run `python3 -m unittest discover -s tests/scap -p 'test_*.py'` after those tests exist. Validate shell syntax with `bash -n` for each new wrapper. Exercise the full workflow on a newly provisioned canary; a second application must avoid unexplained drift or duplicate scheduled jobs. Keep privileged integration checks on isolated RHEL 10 infrastructure. Configure scan frequency, evidence retention, delivery deadline, and an alert for missed/failed scans before rollout.

**Expected result / acceptance:** CI blocks malformed evidence and unsafe default task behavior. A clean-host run reproduces accepted results; repeat execution has documented effects. Rollout proceeds in defined batches only after host access, service, SCAP, and Elastic gates pass for each batch. Stop conditions and the person responsible for rollback are recorded. No automated remediation is added to routine scanning by default.

**Rollback point:** Stop subsequent batches; restore affected hosts and configuration versions using the demonstrated procedure. Preserve all run evidence and open a corrective task before retrying.

**Evidence:** CI output, sanitized fixtures, clean-host/repeat-run results, scan-failure alert test, release commit, batch inventory, gate results, and final evidence-bundle checksum/reference.

## Completion definition

The integration is ready when Task 01 closes source-traceability gaps, Tasks 02–08 have recorded acceptance evidence, and the repository exposes documented runnable entry points for installation, configuration, deployment, scanning, validation, and recovery. This document alone does not establish that those entry points exist or that the environment has passed validation.
