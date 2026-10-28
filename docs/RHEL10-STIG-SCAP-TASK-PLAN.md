# RHEL 10 STIG and SCAP Integration Plan

This plan defines the work required to integrate RHEL 10 security assessment and hardening into the [Elastic Security Engineering project](https://github.com/jbanday808/elastic-security-engineering-rhel10). It follows the implementation sequence from environment preparation and installation through configuration, deployment, and validation. Each step establishes the prerequisites, commands, acceptance criteria, recovery procedure, and evidence required before work can advance.

**Implementation status:** This document is a proposed task plan. The repository guide and existing automation have not been verified because repository access was unavailable during preparation. Step 1 must reconcile this plan with the source guide before implementation begins. The paths and task names below describe proposed deliverables; they do not confirm that those files or commands already exist.

## Validation priorities

The following risks require validation before deployment. They identify questions to resolve rather than confirmed defects in the project.

| Priority | Validation requirement | Required evidence | Steps |
| --- | --- | --- | --- |
| Critical | Confirm that the selected SCAP content includes an applicable RHEL 10 STIG profile. | Record the content source, benchmark revision, profile identifier, supported release, and datastream checksum. | 1–3 |
| Critical | Demonstrate recovery from changes that affect authentication, auditing, firewall rules, cryptography, or boot behavior. | Complete a snapshot restoration and verify console access and a fresh administrative login. | 2, 5–6 |
| Critical | Verify that hardening preserves host access, required services, and Elastic telemetry after reboot. | Capture service checks and a newly generated host event received by Elastic after reboot. | 4, 6–7 |
| High | Distinguish assessment failures from execution failures and incomplete evidence. | Preserve evaluator exit codes and reject missing, malformed, stale, incomplete, or incorrectly attributed results. | 3, 7 |
| High | Account for manual checks, exceptions, exclusions, and unresolved rule results. | Maintain a rule disposition register with evidence, ownership, approval, and expiry where applicable. | 5, 7 |
| High | Ensure that repeated delivery and changes to assessment content remain traceable. | Verify event identity, duplicate handling, content hashes, evidence protection, and source-to-index reconciliation. | 4, 8 |

## Repository and execution requirements

Implement each step as a separate, reviewable repository change. Perform host changes on a disposable RHEL 10 test host until the validation requirements are satisfied. Use the deployment model documented by the project, including its actual choice of Fleet-managed or standalone Elastic Agent.

The proposed repository structure is:

```text
docs/RHEL10-STIG-SCAP-TASK-PLAN.md
docs/rhel10-stig-scap-source-map.md
config/scap/manifest.yaml
config/scap/tailoring.xml
scripts/scap/preflight.sh
scripts/scap/install.sh
scripts/scap/baseline.sh
scripts/scap/generate.sh
scripts/scap/apply.sh
scripts/scap/validate.sh
scripts/scap/normalize.py
tests/scap/fixtures/
tests/scap/test_results.py
```

Use the repository's existing task runner where one is available. Proposed task names are `scap-preflight`, `scap-install`, `scap-baseline`, `scap-generate`, `scap-apply`, and `scap-validate`. Implement and document these entry points before using them. Assessment and fix generation must run without applying remediation. The apply task must require an explicit test-host identifier, change identifier, and verified recovery checkpoint. Run privileged integration checks on isolated RHEL 10 infrastructure.

For each execution, record the UTC start and end times, host identity, RHEL release, repository commit, package versions, selected profile, benchmark revision, datastream and tailoring checksums, command exit codes, and operator or change identifier. Remove secrets from recorded arguments and logs. Store raw assessment results, reports, logs, and configuration backups in a restricted evidence location with defined retention. Commit sanitized fixtures and evidence references to Git, and record a checksum for the completed evidence bundle.

## Step 1 — Establish the implementation baseline

### Prerequisites

Obtain a readable repository checkout, the RHEL 10 STIG/SCAP guide, and any repository-specific contribution or execution instructions.

### Implementation

Review the repository instructions and identify the current source revision, existing automation, and relevant documentation.

```bash
git rev-parse HEAD
git status --short
rg -n -i 'rhel.?10|stig|scap|oscap|remediat|elastic.agent' .
```

Map each installation, configuration, deployment, and validation section of the guide to a step in this plan. Record the source path, section, existing command, and verification method in `docs/rhel10-stig-scap-source-map.md`. Reuse existing scripts and tests where they support the required behavior.

Create a manifest that identifies the supported RHEL minor release and architecture, Elastic versions, Agent deployment model, benchmark source and revision, required services, evidence location, and acceptable telemetry delivery time. Replace draft command placeholders with verified repository commands as they become available.

### Acceptance criteria

This step is complete when every guide section has a corresponding implementation task and verification method. The manifest must identify supported versions and unresolved compatibility issues. Any missing RHEL 10 STIG content or unsupported version combination must block the affected implementation work.

### Rollback and evidence

Revert the isolated documentation change if the baseline requires correction. Retain the source map, repository commit, manifest, and record of outstanding decisions as implementation evidence.

## Step 2 — Verify prerequisites and demonstrate recovery

### Prerequisites

Complete Step 1 and provision a disposable RHEL 10 test host with approved package repositories, administrative privileges, console access, and a documented snapshot and restoration procedure.

### Implementation

Implement a preflight script that verifies the operating system, architecture, privileges, storage capacity, time synchronization, SELinux mode, failed services, and package repository availability.

```bash
cat /etc/redhat-release
uname -m
id
df -h
timedatectl status
getenforce
systemctl --failed
sudo dnf repolist
```

Record the host's DNS and routing configuration, required Elastic destinations, and current authentication, audit, firewall, cryptographic, and Agent settings. Use inspection commands appropriate to the installed services and remove credentials from captured output.

Create a platform snapshot and demonstrate restoration before applying security changes. Document the actual platform commands, restoration duration, and recovery checks. Verify console access and a fresh administrative login after restoration.

### Acceptance criteria

The preflight script must stop when the host has an unsupported operating system, insufficient privileges or capacity, unavailable content sources, or no recovery reference. Restoration must return the host to a usable state with working administrative access. Recovery coverage must include changes affecting boot behavior and filesystems where those changes are in scope.

### Rollback and evidence

Use the demonstrated clean snapshot as the recovery checkpoint. Stop implementation if restoration cannot be verified. Retain the sanitized inventory, preflight results, snapshot identifier, restoration transcript, elapsed recovery time, and access checks.

## Step 3 — Install OpenSCAP and establish the assessment baseline

### Prerequisites

Complete Step 2 and record the approved package and assessment-content sources in the manifest.

### Implementation

Install the assessment tools on the test host and record their versions.

```bash
sudo dnf install -y openscap-scanner scap-security-guide
rpm -q openscap-scanner scap-security-guide
oscap --version
rpm -ql scap-security-guide
```

Identify the RHEL 10 datastream from the installed package contents. Set `DATASTREAM` to its reviewed absolute path and obtain the full profile identifier from the content metadata. Set `PROFILE` to the applicable identifier, then validate and hash the datastream.

```bash
oscap info "$DATASTREAM"
oscap ds sds-validate "$DATASTREAM"
sha256sum "$DATASTREAM"
```

Confirm that the selected content covers the target RHEL release and intended STIG benchmark. If suitable content is unavailable, stop and resolve an approved source before proceeding.

Set `RUN_DIR` to a new, restricted evidence directory and execute the baseline assessment. The wrapper must capture the evaluator's return status even when it is nonzero.

```bash
sudo oscap xccdf eval --profile "$PROFILE" \
  --results-arf "$RUN_DIR/baseline.arf.xml" \
  --report "$RUN_DIR/baseline.html" "$DATASTREAM"
```

### Acceptance criteria

The datastream must validate successfully, and its source, checksum, benchmark revision, profile, and applicability must be recorded. The assessment must evaluate at least one rule and produce results with the correct host identity and timestamps.

Confirm exit-code behavior against the installed OpenSCAP documentation. Exit code `0` normally indicates an evaluation without failing rules, while `2` indicates an evaluation containing failures; other codes require investigation as execution errors. A completed assessment with failing rules provides a usable baseline, but deployment approval depends on the subsequent review and validation steps. Baseline assessment must run without `--remediate`.

### Rollback and evidence

Restore the pre-installation snapshot if package changes require reversal, while preserving the assessment evidence. Retain package versions, content metadata, validation output, exit codes, checksums, baseline ARF and HTML files, evaluator logs, and counts for each rule-result category.

## Step 4 — Configure Elastic ingestion and verify baseline delivery

### Prerequisites

Complete Step 3 and confirm the project's Agent deployment model, approved output destinations, certificate authority, and intended ingestion path.

### Implementation

Follow the guide's verified Agent installation and enrollment commands through a wrapper that protects credentials. Inspect the installed Agent service and use the following command where supported by the installed binary:

```bash
sudo elastic-agent status
```

Validate output connectivity using the configured certificate authority and TLS verification. Implement a documented path for converting completed ARF assessments into JSON records and delivering them through the project's supported integration or ingestion pipeline.

Define the normalized schema before creating mappings. Preserve the host identity, scan identifier, scan timestamps, benchmark and profile identifiers, content version and checksum, rule identifier, severity, and original XCCDF result. Specify the destination index or data stream, event identity, and duplicate-handling policy.

Validate the parser against sanitized fixtures, publish one baseline assessment, and query Elastic for the exact host and scan identifier. Record the actual API or Kibana query once the destination schema is established. Verify ordinary host telemetry independently of SCAP result delivery.

### Acceptance criteria

Both host telemetry and baseline assessment records must be searchable with correct field types, timestamps, and source counts. Malformed input must produce a visible rejection or quarantine result. Repeated delivery of the same assessment must follow the documented duplicate-handling policy, and delivery must meet the time limit established in Step 1.

### Rollback and evidence

Restore the previous Agent policy, output configuration, and pipeline or mapping versions if ingestion changes fail. Use an isolated test destination to protect shared evidence. Retain redacted configuration, schema and pipeline versions, parser results, Agent status, query output, delivery latency, and reconciled record counts.

## Step 5 — Review findings and prepare targeted remediation

### Prerequisites

Complete Steps 3 and 4, review the baseline findings, and obtain the benchmark's requirements for manual assessment.

### Implementation

Assign each failed or unevaluated rule a documented disposition: automated remediation, manual action, further investigation, or proposed exception. For each exception, record the rule identifier, rationale, owner, approval, expiry, and compensating control.

Create and validate tailoring through the workflow supported by the installed OpenSCAP version. Record the effective tailored profile and tailoring checksum. If tailoring changes the baseline selection, rerun the assessment with that tailoring before generating a fix.

Obtain `RESULT_ID` from the relevant assessment document and generate remediation for that specific result.

```bash
oscap xccdf generate fix --fix-type bash \
  --result-id "$RESULT_ID" \
  --output "$RUN_DIR/remediation.sh" "$RUN_DIR/baseline.arf.xml"
bash -n "$RUN_DIR/remediation.sh"
```

Verify that the installed OpenSCAP version accepts the selected input. If it requires extracted XCCDF results, document and validate the supported extraction procedure before generation.

Review the generated changes for effects on authentication, audit collection, firewall reachability, cryptography, TLS, filesystems, boot behavior, and Elastic compatibility. Resolve audit collector ownership conflicts through a supported configuration. Prepare a separate reviewed procedure for controls that require manual changes.

### Acceptance criteria

Every actionable finding must have a disposition. The generated fix must correspond to the reviewed assessment and profile, pass shell syntax validation, and receive a documented change review. Reports must show tailoring exclusions, and manual remediation must have an approved procedure. Fix generation must leave the host configuration unchanged.

### Rollback and evidence

Retain the unchanged test host and the versioned manifest and tailoring as the checkpoint. Revert those configuration files if the selected scope changes. Preserve the disposition register, exception records, tailoring checksum, assessment result identifier, generated fix checksum, syntax-check output, and review record.

## Step 6 — Apply remediation and verify recovery after reboot

### Prerequisites

Complete Step 5 and establish a fresh snapshot, tested console access, an approved change window, and verified assessment-content and remediation checksums.

### Implementation

The apply script must verify the test-host identity, change identifier, recovery reference, reviewed fix checksum, and approved rule dispositions before execution.

```bash
sudo bash "$RUN_DIR/remediation.sh"
```

Capture the command status and restricted execution logs. Stop on a failed or partial execution and assess recovery before continuing. Perform reviewed manual changes separately, then reboot through the documented host or platform procedure when required.

After reconnecting, inspect failed services and verify a fresh administrative login, expected network access, SELinux mode, Agent health, required TLS connections, and the workload checks defined by the guide.

```bash
systemctl --failed
getenforce
```

Generate a new host event after reboot and verify its arrival in Elastic.

### Acceptance criteria

The host must boot successfully and retain working administrative access, required services, TLS connectivity, and telemetry delivery. Access loss, a failed required service, an unexplained configuration change, or interrupted telemetry must trigger rollback and block further deployment.

### Rollback and evidence

Restore the pre-change snapshot and any affected external Agent policy or pipeline versions, then repeat access and telemetry checks. Restore Elastic-side configuration separately because a host snapshot covers only the host. Retain execution logs and status, the snapshot reference, boot time, service and access results, the post-reboot event identifier and timestamp, and any restoration results.

## Step 7 — Validate hardening and reconcile the evidence

### Prerequisites

Complete Step 6 successfully and retain the same datastream and effective tailoring used for the approved baseline.

### Implementation

Repeat the assessment from Step 3 and write the results to separate `post.arf.xml` and `post.html` files. Include the verified tailoring arguments where applicable. Compare the baseline and post-remediation results by rule identifier and result category.

Reconcile the source assessment with normalized and indexed records using the scan identifier. Confirm authentication behavior, audit-event delivery, workload operation, and required TLS connections. Complete manual checks and attach the corresponding evidence and reviewer disposition.

### Acceptance criteria

Targeted remediations must pass or receive a documented investigation and approved disposition before release. There must be no unexplained regression, missing rule, assessment error, unknown result, unchecked rule, or change in applicability. Remaining failures and exclusions must have current approved dispositions, and manual checks must have supporting evidence.

Elastic record counts must reconcile with the assessment under the documented event model. Fresh telemetry must arrive within the delivery time established in Step 1. The final assessment must state automated coverage, manual findings, exceptions, and residual risk; any compliance conclusion requires the relevant review beyond the automated score.

### Rollback and evidence

Use the Step 6 recovery checkpoint when hardening causes a regression, and preserve the failed validation results. When the assessment is valid but delivery fails, correct the ingestion path and repeat reconciliation. Retain the post-remediation ARF and HTML files, evaluator logs and exit code, rule comparison, manual checklist, exception register, query results, reconciled counts, and operational checks.

## Step 8 — Establish regression checks and release in stages

### Prerequisites

Obtain acceptance of Step 7 and complete the recovery and evidence-handling procedures.

### Implementation

Add sanitized fixtures and meaningful regression tests for passing and failing controls, evaluator errors, truncated or empty input, incorrect profile or host identity, stale assessments, exclusions, and repeated delivery. After implementing the test suite, run:

```bash
python3 -m unittest discover -s tests/scap -p 'test_*.py'
```

Validate each new shell script with `bash -n`. Exercise the complete workflow on a newly provisioned RHEL 10 test host, then repeat it to verify documented behavior and detect unintended drift or duplicate scheduled jobs.

Define the assessment schedule, evidence retention period, delivery deadline, and alert behavior for missed or failed assessments. Test the alert before release. Establish deployment batches, stop conditions, and a named rollback owner.

### Acceptance criteria

Automated checks must detect malformed evidence and prevent unsafe default task behavior. A fresh-host execution must reproduce the accepted outcome, and repeated execution must have documented effects. Each deployment batch must pass access, service, SCAP assessment, and Elastic delivery checks before the next batch begins. Routine assessment must remain separate from explicitly authorized remediation.

### Rollback and evidence

Stop subsequent batches when a validation requirement fails. Restore affected hosts and external configuration through the demonstrated recovery procedure, preserve all evidence, and resolve the failure before retrying. Retain CI results, sanitized fixtures, fresh-host and repeat-run results, the alert test, release commit, batch inventory, validation records, and the final evidence-bundle checksum and location.

## Completion criteria

The integration is ready for release when the source guide has been reconciled with this plan, every step has recorded acceptance evidence, and the repository provides documented entry points for preparation, installation, assessment, remediation, validation, and recovery. The release record must identify the supported environment, remaining exceptions, operational owner, and demonstrated rollback procedure.
