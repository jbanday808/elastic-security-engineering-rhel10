# RHEL 10 Security Assessment and Monitoring Plan

This plan explains how the [Elastic Security Engineering project](https://github.com/jbanday808/elastic-security-engineering-rhel10) will check its Linux systems, make reviewed security improvements, and confirm that monitoring continues to work afterward. It turns the project guide into eight ordered tasks, with a clear result required at each stage.

RHEL 10, short for Red Hat Enterprise Linux 10, is the operating system being secured. A STIG is a published checklist of security requirements. SCAP provides a standard way to automate many of those checks, and OpenSCAP is the software that performs them. Elastic collects security information so the team can review system activity and assessment results in one place. The repository is the project's shared collection of code and documentation.

The intended outcome is a repeatable process that improves security, preserves access and monitoring, and produces records that a reviewer can verify. Some requirements still need a person to assess them, so an automated scan alone cannot establish full compliance.

**Plan status:** This is a proposed plan. The existing repository guide and automation still need to be checked against it in Step 1. The task names and file locations in the technical reference describe work to be implemented; they do not establish that the tools already exist or that testing has passed.

## Resolve the most serious risks first

Before changing a system, the team must establish that it is using the right security checklist and can recover if a change causes problems. These are questions to resolve during implementation, rather than confirmed problems with the project.

| Priority | What the team must establish | Why it matters |
| --- | --- | --- |
| Critical | The selected security checklist applies to the exact RHEL 10 version being tested. | An assessment can produce misleading results when it uses the wrong checklist. |
| Critical | The team can restore the test system and regain administrative access. | Security changes can affect sign-in, network access, and the system's ability to start. |
| Critical | Required services and Elastic monitoring still work after a restart. | A running monitoring program does not prove that new information is reaching Elastic. |
| High | The assessment finished successfully and belongs to the correct system and date. | A broken or incomplete scan can be mistaken for a useful assessment. |
| High | Every unresolved requirement has a documented next step or an approved exception. | A favorable overall score can hide individual requirements that still need attention. |
| High | Assessment records are complete, protected, and handled consistently when sent more than once. | Missing or repeated records can distort reporting, and raw results can expose sensitive system details. |

## Step 1 — Confirm the scope and starting point

**Before starting:** The project team needs access to the repository, the original guide, and the instructions for contributing changes.

**What the team will do:** The team will connect each part of the guide to a task in this plan and identify any scripts or tests that can be reused. It will record the RHEL and Elastic versions, the approved security checklist, the services that must remain available, and where assessment records will be kept. It will also define how quickly new security information must appear in Elastic.

**Ready to move on:** Every guide section must have an assigned task and a way to check the result. The team must identify unsupported software combinations and resolve them before the affected work begins.

**If a correction is needed:** The team can revise or reverse this documentation change before making system changes.

**What to keep:** Retain the guide-to-task mapping, the exact repository revision, the agreed system versions, and any decisions that remain open.

## Step 2 — Prepare a test system and prove that it can be restored

**Before starting:** Step 1 must be complete. The team needs a separate RHEL 10 test system, permission to administer it, access to approved software sources, and access through a recovery console, which remains available if normal remote access fails.

**What the team will do:** The team will check storage, system time, network access, existing security settings, and service health. It will then save a recovery snapshot, which captures the system's state, and demonstrate that the snapshot can be restored. After restoration, an administrator must be able to sign in again through both the normal connection and the recovery console.

**Ready to move on:** The readiness check must stop work when essential prerequisites are missing. Restoration must return the system to a working state, with recovery time recorded. The recovery method must cover the startup and storage changes that are in scope.

**If something goes wrong:** Stop and correct the recovery procedure before installing tools or applying security changes.

**What to keep:** Retain the readiness results, snapshot reference, restoration record, recovery time, and confirmation that administrative access works.

## Step 3 — Install the assessment tools and record the initial results

**Before starting:** Step 2 must be complete, and the team must have approved sources for the assessment software and security checklist.

**What the team will do:** The team will install OpenSCAP and confirm that its security content applies to the intended RHEL 10 release and STIG version. It will then assess the test system without changing its settings. This first assessment becomes the baseline: a record of the system before security improvements are applied.

**Ready to move on:** The assessment must finish, check the expected requirements, and identify the correct system and time. The team must distinguish between a completed assessment that found weaknesses and a scan that failed to run correctly. If an appropriate RHEL 10 STIG checklist is unavailable, the affected work must stop until an approved source is established.

**If something goes wrong:** Preserve the results for investigation. Restore the earlier snapshot if the tool installation needs to be reversed.

**What to keep:** Retain the tool and checklist versions, the original assessment results, the readable report, and the execution record showing whether the assessment completed.

## Step 4 — Connect the results to Elastic and confirm delivery

**Before starting:** Step 3 must be complete. The team must confirm how the project installs and manages Elastic Agent, the software that collects information from the system.

**What the team will do:** The team will configure secure delivery of system activity and assessment results to Elastic. It will define a consistent record format so each finding can be traced to its system, assessment, checklist version, and individual requirement. It will then search Elastic to confirm that the expected information arrived.

**Ready to move on:** Both system activity and assessment results must be visible within the agreed delivery time. The assessment records must match the source report under the agreed reporting format. Incomplete or unreadable input must produce a visible error, and sending the same assessment again must follow the documented rules for repeated records.

**If something goes wrong:** Restore the previous monitoring settings and result-processing configuration. Use a separate test destination to protect existing project records.

**What to keep:** Retain configuration records with credentials removed, sample search results, delivery times, record counts, and the results of input-processing tests.

## Step 5 — Review the findings and choose the changes

**Before starting:** Steps 3 and 4 must be complete. The team needs the initial findings and the checklist's instructions for requirements that need human review.

**What the team will do:** The team will decide how to address each unresolved requirement. Some findings can be corrected automatically, while others require a manual change, further investigation, or an approved exception. The team will review proposed changes for their effect on sign-in, networking, system startup, and Elastic monitoring. Preparing a change script will leave the system's settings unchanged.

**Ready to move on:** Every actionable finding must have a documented decision. Each proposed exception must identify an owner, a reason, an approval, an expiry date, and an alternative measure to reduce risk. Any change to the selected checklist requirements must be recorded and reflected in a new baseline before generating the corresponding change script. The script and any manual procedures must be reviewed before use.

**If a correction is needed:** Revise the checklist selections or proposed changes while retaining the unchanged test system as the starting point.

**What to keep:** Retain the finding-by-finding decisions, exception records, selected requirements, proposed change script, and review record.

## Step 6 — Apply the reviewed changes and restart the test system

**Before starting:** Step 5 must be complete. The team needs a fresh recovery snapshot, working console access, an agreed maintenance window, and confirmation that the proposed changes match the reviewed version.

**What the team will do:** The team will apply the reviewed changes to the designated test system and record what happened. It will stop if execution fails or completes only part of the work. After restarting the system when required, it will verify sign-in, network access, required services, and monitoring. It will generate a new system event and confirm that Elastic receives it after the restart.

**Ready to move on:** The system must start successfully, remain accessible, and continue providing its required services. Secure connections and new monitoring information must work within the agreed limits.

**If something goes wrong:** Loss of access, a failed required service, interrupted monitoring, or an unexplained change must stop further deployment. Restore the saved system state and any affected Elastic settings, then verify access and monitoring again. Restoring the system alone does not reverse changes made separately in Elastic.

**What to keep:** Retain the change record, execution results, snapshot reference, restart time, service and access checks, and the new event received by Elastic. Record any restoration that was necessary.

## Step 7 — Confirm the improvements and account for remaining findings

**Before starting:** Step 6 must have passed its checks. The follow-up assessment must use the same approved checklist and selections as the baseline.

**What the team will do:** The team will assess the system again and compare the individual requirements before and after the changes. It will investigate unexpected differences, complete the manual checks, and verify that Elastic contains the corresponding results. It will also confirm that ordinary system activity continues to arrive.

**Ready to move on:** Each targeted finding must be resolved or have a reviewed and approved explanation. Missing checks, assessment errors, unexplained results, or newly introduced problems must be addressed before release. All remaining exceptions must be current, and manual checks must have supporting records. The final report must explain what was checked, what remains unresolved, and what risk is being accepted.

**If something goes wrong:** Restore the saved system state when a security change causes an operational problem. If the assessment is sound but its delivery to Elastic fails, repair the delivery process and check the records again. Preserve the failed validation results for investigation.

**What to keep:** Retain the follow-up report, the requirement-by-requirement comparison, manual review records, approved exceptions, and confirmation that Elastic's results match the source assessment.

## Step 8 — Make the process repeatable and expand gradually

**Before starting:** Step 7 must be accepted, and the recovery procedure and handling of assessment records must be documented.

**What the team will do:** The team will test the full process on a newly prepared RHEL 10 system and repeat it to check for unintended changes or duplicate scheduled work. It will add automated checks for incomplete results, incorrect system details, repeated records, and other known failure cases. Before expanding to more systems, it will define the assessment schedule, record-retention period, delivery deadline, and alerts for missed or failed assessments.

**Ready to expand:** The process must produce consistent results, and the team must demonstrate that failure alerts work. Each deployment group must pass access, service, assessment, and monitoring checks before the next group begins. A named person must be responsible for recovery. Scheduled assessments must remain separate from explicitly approved changes to system settings.

**If something goes wrong:** Stop the next deployment group, restore affected systems and settings where needed, and resolve the cause before trying again.

**What to keep:** Retain the test results, alert demonstration, approved repository revision, list of affected systems, deployment decisions, and final assessment records.

## What completion means

The integration is ready when the plan matches the source guide, each step has recorded results that meet its acceptance criteria, and another team member can follow the documented process. The handover must identify the supported environment, remaining exceptions, operational owner, assessment schedule, and demonstrated recovery procedure.

For every assessment or change, keep enough information to establish who performed it, which system and software versions were involved, when it ran, and what happened. Protect raw reports and backups because they can reveal sensitive system details. Place only examples with sensitive information removed and references to restricted evidence in the public repository.

## Technical reference for the implementation team

The commands and proposed file locations below support the eight steps above. The engineer carrying out the work must check them against the actual guide, installed software versions, and deployment platform before implementing the repository tasks. Environment-specific commands for snapshots, Agent enrollment, certificate checks, tailoring, and Elastic searches must be documented during implementation.

<details>
<summary>Expand the commands and repository requirements.</summary>

### Proposed repository files and tasks

Use the project's existing task runner and deployment model where available. The following paths are proposed deliverables.

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

Proposed task names are `scap-preflight`, `scap-install`, `scap-baseline`, `scap-generate`, `scap-apply`, and `scap-validate`. Implement them before use. Keep assessment, fix generation, and remediation separate. The apply task must verify the test-host identifier, change identifier, approved script checksum, and recovery reference before execution. Privileged integration tests must run on isolated RHEL 10 infrastructure.

### Step 1 commands

Run these commands from the repository checkout after reading its instructions.

```bash
git rev-parse HEAD
git status --short
rg -n -i 'rhel.?10|stig|scap|oscap|remediat|elastic.agent' .
```

The manifest must record the RHEL minor release and architecture, Elastic versions, Fleet-managed or standalone Agent mode, benchmark source and revision, required services, evidence location, and delivery deadline. Map each guide section to a repository command and verification method.

### Step 2 commands

Run the readiness checks on the test system and add the platform-specific recovery procedure to the runbook.

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

Also record DNS, routing, required Elastic destinations, and the current authentication, audit, firewall, cryptographic, and Agent settings. Verify normal login and console recovery after a demonstrated snapshot restoration. A configuration backup alone does not establish recovery from boot or filesystem changes.

### Step 3 commands

Install the packages from approved sources and record their versions.

```bash
sudo dnf install -y openscap-scanner scap-security-guide
rpm -q openscap-scanner scap-security-guide
oscap --version
rpm -ql scap-security-guide
```

Set `DATASTREAM` to the reviewed absolute path of the RHEL 10 datastream. Read its metadata, select the applicable full profile identifier as `PROFILE`, and set `RUN_DIR` to a new restricted absolute evidence directory. Package installation does not establish that a suitable RHEL 10 STIG profile is included.

```bash
oscap info "$DATASTREAM"
oscap ds sds-validate "$DATASTREAM"
sha256sum "$DATASTREAM"

sudo oscap xccdf eval --profile "$PROFILE" \
  --results-arf "$RUN_DIR/baseline.arf.xml" \
  --report "$RUN_DIR/baseline.html" "$DATASTREAM"
```

Capture the evaluator's return status even when it is nonzero. Confirm the installed OpenSCAP version's exit-code behavior: `0` normally indicates an evaluation without failing rules, while `2` indicates an evaluation containing failures. Investigate other codes as execution errors. Validate the expected rule coverage, host identity, and timestamps. Preserve counts for each result category, including failed, error, unknown, unchecked, not applicable, and excluded requirements. Run the baseline without `--remediate`.

### Step 4 implementation requirements

Use the guide's verified installation and enrollment commands for the actual Agent deployment model. Keep tokens out of Git and recorded output. Inspect the installed service and use this status command where supported.

```bash
sudo elastic-agent status
```

Verify TLS with the configured certificate authority. Define the ARF-to-JSON schema and destination index or data stream before configuring mappings. Retain the host identity, scan identifier, timestamps, benchmark and profile identifiers, content version and checksum, rule identifier, severity, and original XCCDF result.

Use stable event identities and a documented duplicate-handling policy. Test malformed input and repeated delivery with sanitized fixtures. Record the exact API or Kibana query for the selected host and scan, and reconcile source, normalized, and indexed counts under the documented event model. Check ordinary host telemetry separately.

### Step 5 commands

Validate tailoring through the installed OpenSCAP version's supported workflow. Pass the verified tailoring arguments to the assessments when applicable and record the effective profile and tailoring checksum. Rerun the baseline if the selected requirements change.

Set `RESULT_ID` from the reviewed assessment document, then generate and syntax-check the proposed fix.

```bash
oscap xccdf generate fix --fix-type bash \
  --result-id "$RESULT_ID" \
  --output "$RUN_DIR/remediation.sh" "$RUN_DIR/baseline.arf.xml"
bash -n "$RUN_DIR/remediation.sh"
```

Confirm that the installed version accepts the input format. If extracted XCCDF results are required, document and validate extraction before generation. Review all generated actions, including audit collector ownership conflicts, and document separate procedures for manual changes. Hash the reviewed script and record its approval.

### Step 6 commands

Run the reviewed script only after the apply task has verified the host, approved change, checksum, and recovery checkpoint.

```bash
sudo bash "$RUN_DIR/remediation.sh"
```

Preserve the exit status and logs, and stop on partial execution or failure. Reboot through the documented platform procedure when required. Verify normal login, console access, network reachability, workload services, Agent health, and TLS connectivity. Include these checks after restart.

```bash
systemctl --failed
getenforce
```

Generate a fresh post-reboot event and capture its identifier and arrival time in Elastic. Restore external Agent policies and pipeline versions separately when rollback requires it.

### Step 7 commands

Repeat the assessment with the same approved content and effective profile. Add the verified tailoring arguments when applicable, and preserve the exit status as in Step 3.

```bash
sudo oscap xccdf eval --profile "$PROFILE" \
  --results-arf "$RUN_DIR/post.arf.xml" \
  --report "$RUN_DIR/post.html" "$DATASTREAM"
```

Compare each rule's result and account for coverage and applicability changes. Complete manual checks, verify current exceptions, reconcile indexed results against source records, and confirm new ordinary telemetry within the agreed deadline. Document automated coverage and remaining risk before any compliance conclusion.

### Step 8 commands

Implement meaningful tests for passing and failing controls, execution errors, empty or truncated input, incorrect profile or host identity, stale assessments, exclusions, and repeated delivery. After the tests exist, run the suite.

```bash
python3 -m unittest discover -s tests/scap -p 'test_*.py'
```

Check each shell script with `bash -n`. Test fresh-host execution, repeated execution, failure alerts, and batch stop conditions. Keep routine scanning separate from remediation.

### Evidence requirements

For each run, retain UTC start and end times, host identity, RHEL release, repository commit, package versions, selected profile, benchmark revision, datastream and tailoring hashes, redacted command arguments, exit codes, and operator or change identifier. Store raw ARF/XML, HTML reports, logs, and configuration backups outside Git in a restricted location with defined retention. Record the final evidence-bundle checksum and location, and commit only sanitized fixtures and evidence references.

</details>

