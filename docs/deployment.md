# RHEL 10 Elastic Security Home Lab Deployment Guide

This guide expands the project's safe deployment summary into installation, configuration, testing, and verification steps. Repository configurations, ES|QL queries, and captured screenshots are the primary evidence. Commands below are instructions for the lab machines; they have not been executed against those machines during this documentation update.

**Evidence terminology:** **Verified** means supported by the repository or a captured screenshot, not a live health assertion. **Unverified** means a configuration, action, or outcome still needs confirmation. **Planned/optional** means outside the demonstrated deployment. Expected command results are acceptance criteria, not recorded execution results.

Use an account with administrative access on each RHEL guest and appropriate permissions in Elastic Cloud. Keep passwords, tokens, API keys, and confidential configuration outside the repository. Do not publish enrollment-token installation commands, terminal captures containing credentials, or unreviewed deployment notes.

## Step 1: Environment Overview

| Component | Lab role and evidence |
|---|---|
| Windows 11 Enterprise | VMware host platform specified for this lab; build and hardware inventory are not recorded in the repository |
| VMware Workstation Pro | Runs the RHEL guests; exact Workstation version and VM resource allocations are not recorded |
| Red Hat Enterprise Linux 10 | Guest operating system on both virtual machines |
| `node1.domain250.example.com` | Endpoint generating system logs, authentication records, and Elastic Defend process events |
| `logstash1.domain250.example.com` | Separate Logstash host, also monitored by its own Elastic Agent |
| Elastic Cloud Serverless Security project | Managed collection, Elasticsearch storage/search, Kibana investigation, and Fleet management; no local Elasticsearch or Kibana installation is documented |
| Elastic Agent 9.5.5 | Fleet-managed collection and endpoint integrations on the RHEL hosts |
| System and Elastic Defend integrations | Operating system monitoring and endpoint visibility |
| Logstash 9.5.5 | Local JSON test pipeline plus separately collected application logs and monitoring metrics |
| ES|QL and Kibana dashboards | Querying and visualization of collected security and performance records |

Run the following on **each RHEL guest**:

```bash
cat /etc/redhat-release
```

Confirms the installed RHEL release. Expect RHEL 10; record the actual minor release rather than assuming one.

```bash
hostnamectl
```

Displays the static hostname, operating system, kernel, and virtualization information.

```bash
ip -brief address
```

Shows interface addresses. Confirm the intended guest network has an address distinct from the other VM.

```bash
ip route
```

Displays routing, including the default route needed for outbound access.

```bash
getent hosts artifacts.elastic.co
```

Checks name resolution for the Elastic download service. A resolved address confirms DNS resolution, not full connectivity to every required service.

```bash
curl -I --connect-timeout 10 https://artifacts.elastic.co/
```

Checks HTTPS reachability and certificate validation. An HTTP response demonstrates a connection even if the server rejects a request to its root URL. Also verify access to the actual Fleet and output destinations provided by your project.

```bash
lscpu
```

Shows processor architecture and assigned CPUs. The Agent archive in Step 4 requires `x86_64`.

```bash
free -h
```

Shows total and available memory. Check capacity before running both guests and their services; no specific RAM allocation is established by the project files.

```bash
df -h / /var /tmp
```

Shows free space for the OS, service data, and downloads.

## Step 2: Configure RHEL 10 Virtual Machines

### Open and configure the guests

1. In Windows 11 Enterprise, open VMware Workstation Pro.
2. Select **File > Open** and choose the existing Node1 VM configuration, or create a RHEL 10 VM using your licensed installation media if rebuilding the lab.
3. With the VM powered off, open its settings. Review CPU, memory, disk, and network adapter settings against available host resources. The repository does not record exact allocations or whether NAT, bridged, or a custom VMware network was used.
4. Select a network that provides the lab's required connectivity. Keep both guests on compatible networks while giving each a unique address. Confirm the network adapter is connected when the VM starts.
5. Start Node1, sign in, and complete the hostname and network checks below.

### Create Logstash1 as a full clone

The lab workflow calls for Logstash1 to be a full clone of Node1. The source files do not preserve the clone wizard history; the following is a reconstruction procedure, not proof of the original clicks.

1. Shut down Node1 before cloning. Prefer cloning a clean guest **before** Elastic Agent installation.
2. In Workstation, select Node1 and open **VM > Manage > Clone**. Select the appropriate powered-off state or snapshot, then **Create a full clone** rather than a linked clone.
3. Name the clone `logstash1`, choose its storage location, and finish the wizard. If VMware asks whether the VM was moved or copied, identify it as copied so VMware generates a new VM identity.
4. Verify that the clone has a distinct virtual NIC MAC address, Linux machine identity, hostname, network address, and SSH host identity. VMware generating a new VM identity does not by itself regenerate every identity stored inside the guest OS.
5. If Node1 already had Elastic Agent installed, the clone may contain copied enrollment state. Do not treat it as a second enrolled endpoint. Rebuild from a clean pre-enrollment image or follow the supported Agent uninstall/reinstall workflow on the clone, checking Fleet records before removing anything. Enroll Logstash1 separately in Step 4; a hostname change alone does not create a unique Agent identity.

On **Node1 only**:

```bash
sudo hostnamectl set-hostname node1.domain250.example.com
```

Sets Node1's documented static hostname.

On **Logstash1 only**:

```bash
sudo hostnamectl set-hostname logstash1.domain250.example.com
```

Sets the clone's distinct hostname. Do not run both hostname-setting commands on one guest.

On **each guest**:

```bash
hostname -f
```

Checks the fully qualified hostname. If it differs from the intended name, check DNS and local hostname resolution.

```bash
nmcli device status
```

Identifies the active network device and its NetworkManager connection.

```bash
nmcli connection show --active
```

Lists active connection profiles. Record the actual profile name; do not assume the same name exists on both guests.

```bash
nmcli device show
```

Displays IP configuration, gateway, and DNS information. Compare the results with the lab's intended addressing.

For changes, use the interactive NetworkManager editor from the VMware console:

```bash
sudo nmtui
```

Select **Edit a connection**, choose the actual profile, and configure DHCP or the lab's assigned static address, gateway, and DNS settings. Apply the profile through **Activate a connection** if necessary. The repository does not establish a complete addressing plan, so no static addresses are prescribed here. Network changes can disconnect a remote terminal.

```bash
cat /etc/machine-id
```

Compare locally on the two guests; their machine IDs must differ. If they match, resolve the clone identity using the RHEL-supported cloning process before enrollment. Keep machine identifiers out of public diagnostic captures.

Repeat the address, route, DNS, and HTTPS checks from Step 1. Review SSH host-key fingerprints if the clone copied existing SSH keys; do not distribute a cloned guest with duplicate host keys.

## Step 3: Configure Elastic Cloud Serverless

1. Sign in to Elastic Cloud using your private account.
2. Open the existing **Security** Serverless project. When rebuilding, create a Security project, selecting a suitable name and region; the sanitized repository does not prescribe account identifiers or project provisioning settings.
3. Launch the project's Elastic Security interface. Confirm that you can access Discover, Dashboards, and security management features.
4. Use navigation search or the management menu to open **Fleet**. Menu placement can change between UI versions.
5. Review **Agent policies**, **Agents**, and project-provided Fleet connection instructions. Use the managed endpoints provided by the project; this lab does not document deploying a separate self-managed Fleet Server VM.
6. Confirm that your user can manage policies and integrations. Follow Step 5 to prepare the target policies before enrolling the hosts in Step 4.

Elasticsearch and Kibana are provided through Elastic Cloud Serverless. Do not install their RPMs on the RHEL guests as part of this guide. Fleet provides central policy management for the agents; see the [official Fleet overview](https://www.elastic.co/docs/reference/fleet).

## Step 4: Install Elastic Agent 9.5.5 on RHEL 10

Run these preparation commands on each guest that needs a fresh Agent installation. Check first for an existing installation; do not install a second copy over a running managed agent. Confirm `curl` and `tar` are available, outbound HTTPS works, the architecture is `x86_64`, and there is sufficient disk space.

```bash
cd /tmp
```

Moves to the temporary download directory.

```bash
curl -fLO https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.5.5-linux-x86_64.tar.gz
```

Downloads the specified Linux x86-64 archive and reports an error for an unsuccessful HTTP response. If this historical version is unavailable, stop and verify availability rather than silently substituting another release. Check the download against Elastic's published checksum before extraction.

```bash
tar -xzvf elastic-agent-9.5.5-linux-x86_64.tar.gz
```

Extracts the downloaded archive without changing the installation on the host.

```bash
cd elastic-agent-9.5.5-linux-x86_64
```

Enters the extracted Agent directory.

### Install and enroll privately through Fleet

In Fleet, select **Add agent**, choose the intended policy, and select the Linux installation instructions. Confirm that the instructions match the intended Agent release. Execute the project-generated installation/enrollment instruction privately on the correct host with the requested privileges. Enroll each VM independently.

**Do not copy the generated enrollment instruction into this guide, GitHub issues, screenshots, or public terminal logs.** Enrollment tokens and active connection credentials must stay outside the repository. This document intentionally contains no enrollment-token installation command, including one with a placeholder. Generate a new token through Fleet when required and handle it through your private deployment process.

After installation:

```bash
sudo systemctl status elastic-agent
```

Checks the Agent service. Expect `active (running)` after successful installation; service activity alone does not prove that all integrations are healthy.

```bash
sudo elastic-agent status --output full
```

Checks the Agent and component states. Review failures or degraded components and compare with Fleet's reported state.

```bash
sudo systemctl is-enabled elastic-agent
```

Checks boot enablement. Expect `enabled` for the intended persistent service installation.

## Step 5: Configure Fleet and Agent Policies

1. Open **Fleet > Agent policies**. Create or select the policy for each host before enrollment. The documented Logstash1 policy is **`logstash1-monitoring`**; the repository does not establish the exact Node1 policy name.
2. Add **System** to collect operating system logs and performance metrics. Enable the required system and authentication log inputs, with paths appropriate to the guest's actual logging configuration.
3. Add **Elastic Defend** to the policies for endpoint monitoring, following Step 6.
4. Add the **Logstash** integration to `logstash1-monitoring`, following Step 10. This integration monitors Logstash; it does not configure the local Logstash pipeline's output.
5. Save the policies. In **Fleet > Agents**, confirm that each VM appears once with its own Agent ID and the intended hostname, version, and policy assignment.
6. Open Logstash1's details. Confirm **Healthy**, a recent last check-in, and the applied policy revision. Figure 1 captures a Healthy Logstash1 agent; Figure 5 shows integration settings. These screenshots establish historical state only.

Policy assignments should follow the host's role. Verify that Node1 process data and Logstash1 monitoring data come from their respective hosts rather than a copied Agent identity.

## Step 6: Configure Elastic Defend

1. In **Integrations**, locate **Elastic Defend** and add it to the applicable RHEL agent policy.
2. Select the endpoint configuration appropriate to the Linux server workload. Save the policy and allow the enrolled agents to receive the update.
3. Review process/security event collection and protection settings. Do not infer that every prevention feature is enabled from the presence of the integration alone.
4. In Fleet, check the Agent's Elastic Defend component for errors.
5. In Elastic Security, open **Endpoints** through navigation search or the management area. Check for the expected host, recent activity, and policy application status.
6. In Discover, run the process query in Step 11, filtering for the intended hostname. Confirm recent process records with fields such as user, process name, command line, and event action.

The repository demonstrates endpoint process collection on Node1 and Logstash1. Exact protection preset settings, prevention tests, and automated response outcomes are not preserved as verified configuration. Refer to [Elastic Defend configuration](https://www.elastic.co/docs/solutions/security/configure-elastic-defend) and the [support matrix](https://www.elastic.co/support/matrix) when checking compatibility for the actual Agent release, kernel, and architecture.

## Step 7: Install Logstash 9.5.5

Perform this step on **Logstash1 only**. The repository documents version 9.5.5, but it does not contain an RPM installation transcript. The following reproduces installation using Elastic's official 9.x package repository, with an explicit version check. Check for an existing Elastic repository definition before adding another one.

```bash
sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```

Imports Elastic's package signing key. Compare its fingerprint with the official installation documentation before trusting packages.

```bash
sudo tee /etc/yum.repos.d/logstash.repo > /dev/null <<'REPO'
[logstash-9.x]
name=Elastic repository for 9.x packages
baseurl=https://artifacts.elastic.co/packages/9.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
REPO
```

Creates the 9.x RPM repository definition with signature checking enabled. Review an existing file before replacing it.

```bash
sudo dnf --showduplicates list logstash
```

Lists available package versions. Confirm that 9.5.5 is available before continuing. If unavailable, resolve the version mismatch rather than installing the latest 9.x release by accident.

```bash
sudo dnf install logstash-9.5.5
```

Installs the requested package version. Review DNF's transaction summary and confirm the selected version before accepting it.

```bash
/usr/share/logstash/bin/logstash --version
```

Verifies the installed executable. Expect the output to identify Logstash 9.5.5.

Configure the pipeline in Step 8 **before enabling the service for a fresh installation**. Once its configuration validates:

```bash
sudo systemctl enable --now logstash
```

Enables Logstash at boot and starts it immediately.

```bash
sudo systemctl status logstash
```

Checks startup status. Expect `active (running)`; use the logs and API checks in Step 9 to verify pipeline readiness.

Repository installation details follow [Elastic's Logstash installation documentation](https://www.elastic.co/docs/reference/logstash/installing-logstash). These commands install Logstash on the guest; they do not install a local Elasticsearch cluster.

## Step 8: Configure the Logstash JSON Test Pipeline

The verified repository configuration is [46-local-test.conf.example](../examples/logstash/46-local-test.conf.example). Its destination on Logstash1 is `/etc/logstash/conf.d/46-local-test.conf`. The configuration's presence is verified; a successful local test execution is not established by the screenshots.

On a fresh installation, prepare the files before the service's first start. For an existing installation, review existing pipelines and stop the service before configuration validation so a second Logstash process does not compete for its data directory.

```bash
sudo systemctl stop logstash
```

Stops the installed service for configuration work. This interrupts processing on an existing instance; use a suitable maintenance window.

```bash
sudo install -d -o root -g logstash -m 0750 /etc/logstash/conf.d
```

Creates the pipeline configuration directory with access for the service group.

```bash
sudo install -d -o logstash -g logstash -m 0750 /var/lib/logstash/lab
```

Creates the local output directory owned by the Logstash service user.

From a checkout of this repository on Logstash1, run:

```bash
sudo install -o root -g logstash -m 0640 examples/logstash/46-local-test.conf.example /etc/logstash/conf.d/46-local-test.conf
```

Copies the safe example to its runtime location. Review and preserve any existing destination file first. If the repository is elsewhere, transfer only this sanitized example and adjust the source path.

The copied file contains:

```logstash
# Example only: local JSON pipeline; does not forward to Elasticsearch.
input {
  tcp {
    id => "rhel10_tcp_input"
    host => "127.0.0.1"
    port => 5055
    codec => json
  }
}
filter {
  mutate {
    add_field => { "[event][dataset]" => "logstash.lab" }
  }
}
output {
  file {
    id => "rhel10_file_output"
    path => "/var/lib/logstash/lab/events.jsonl"
    codec => json_lines
    file_mode => 0640
  }
}
```

The TCP input decodes JSON, the filter labels the event dataset as `logstash.lab`, and the output writes one JSON event per line. Port `5055` binds to `127.0.0.1`, so it accepts connections from Logstash1 itself. Do not open a firewall port or use another VM as the sender for this loopback-only test. There is no Elasticsearch output in this configuration.

```bash
sudo cat /etc/logstash/pipelines.yml
```

Checks how the service loads pipelines. Confirm the intended pipeline includes `/etc/logstash/conf.d/*.conf` through `path.config`. Review other files matched by that path because they can be combined into the same pipeline. Do not replace existing pipeline definitions without reviewing their purpose.

```bash
sudo -u logstash /usr/share/logstash/bin/logstash --path.settings /etc/logstash --config.test_and_exit -f /etc/logstash/conf.d/46-local-test.conf
```

Validates this pipeline as the service user while Logstash is stopped. Expect a successful configuration validation and exit. This explicit `-f` check tests the named file; it does not prove that every configuration loaded by the service is valid or that events have flowed.

Start the service using Step 7's enable/start command and wait until Step 9 shows a listening input. Then send a synthetic event **from Logstash1**:

```bash
bash -c 'printf "%s\n" "{\"message\":\"rhel10-local-json-test\"}" > /dev/tcp/127.0.0.1/5055'
```

Uses Bash's TCP support to send a newline-terminated JSON record. This creates test data only and does not send it to Elastic Cloud.

```bash
sudo tail -n 10 /var/lib/logstash/lab/events.jsonl
```

Checks for the test message and the added dataset field. Allow time for the pipeline to write the event. Finding the event verifies local input, processing, and file output; it does not verify Elasticsearch forwarding.

## Step 9: Verify Logstash Services and Connectivity

Run each check on Logstash1:

```bash
sudo systemctl status logstash
```

Checks whether the service is running and shows recent service messages.

```bash
sudo ss -lntp | grep ':5055'
```

Checks the TCP listener. Expect `127.0.0.1:5055` associated with the Logstash Java process. A wildcard listener would not match the documented loopback-only configuration.

```bash
curl -sS 'http://127.0.0.1:9600/?pretty'
```

Queries the local Logstash API. Expect a JSON response identifying the running instance. API availability alone does not prove the test pipeline is loaded.

```bash
sudo tail -n 10 /var/log/logstash/logstash-plain.log
```

Reviews recent application messages for pipeline startup, listening input, configuration errors, or output failures.

```bash
curl -sS 'http://127.0.0.1:9600/_node/stats/pipelines?pretty'
```

Inspects pipeline statistics. Compare event counters before and after sending the local JSON test. Idle pipelines can legitimately show zero activity.

Use the local output check in Step 8 to confirm file delivery. Figures 6–12 document historical Logstash health and performance, including periods with no pipeline activity; they do not substitute for a new local test.

## Step 10: Configure Logstash Monitoring Integration

1. In Fleet, open `logstash1-monitoring` and add or edit the **Logstash** integration.
2. Enable **Metrics (Elastic Agent)** and **Logs**. Figure 5 shows these enabled and **Metrics (Stack Monitoring)** disabled.
3. Expand the metric settings and verify the local API target, normally `http://127.0.0.1:9600` for the same-host agent. The API checks in Step 9 must work before metric collection can succeed.
4. Review the application log paths against the actual files in `/var/log/logstash/`, including `logstash-plain.log`. Ensure that the Agent can read the configured files.
5. Save the integration and verify that Logstash1 receives the updated policy and remains Healthy.
6. Use Discover to confirm application logs and datasets such as `logstash.node`, `logstash.pipeline`, `logstash.plugins`, and `logstash.health_report` where supplied by the installed integration version.

The integration collects node and pipeline information used for CPU, JVM heap, event counts, throughput, queue, and health views. Available datasets and field names depend on the installed package version; verify them in Discover rather than assuming every dataset is present.

This project uses Elastic Agent monitoring data and custom Kibana dashboards. Stack Monitoring is a separate collection/UI workflow and is not established by these screenshots. Do not enable both metric modes simply to reproduce the documented dashboard. See the [official Logstash integration reference](https://www.elastic.co/docs/reference/integrations/logstash/) for mode and configuration details.

## Step 11: Verify Data Collection in Kibana Discover

Open **Discover**, switch to **ES|QL**, select a time range that includes known activity, and run one query at a time. These queries use the repository's data sources, with simple standalone examples that do not require dashboard time parameters.

### Logstash metrics

```esql
FROM metrics-logstash.*
| STATS records = COUNT(*) BY data_stream.dataset, host.name
| SORT records DESC
```

Counts metrics by dataset and host. Nonzero results confirm ingested monitoring documents in the selected range. Inspect dataset names and host attribution; they do not prove custom pipeline events were forwarded. This matches [metrics-datasets.esql](../queries/logstash/metrics-datasets.esql) and Figure 2.

### Logstash application logs

```esql
FROM logs-logstash.log-*
| SORT @timestamp DESC
| LIMIT 20
| KEEP @timestamp, host.name, message
```

Shows recent Logstash application messages. Look for the intended hostname and pipeline/service messages. Figure 3 supports successful application-log collection.

### Endpoint process events

```esql
FROM logs-endpoint.events.process-*
| WHERE host.name == "node1.domain250.example.com"
| SORT @timestamp DESC
| LIMIT 20
| KEEP @timestamp, host.name, user.name, process.name, process.command_line, event.action
```

Shows process activity collected by Elastic Defend on Node1. Substitute Logstash1's documented hostname when checking that host. Figure 4 supports Logstash1 process collection; Figures 13–19 show Node1 activity.

### System authentication logs

```esql
FROM logs-system.auth-*
| SORT @timestamp DESC
| LIMIT 20
| KEEP @timestamp, host.name, user.name, event.action, event.outcome, source.ip, message
```

Shows authentication-related log records. Check the original message alongside parsed fields. Missing source addresses and `unknown` outcomes can be normal for local or uncategorized records. Figures 20–26 show captured authentication activity, not a guarantee of a particular event count in a new window.

The full [query collection](../queries/) contains dashboard queries. Files using `?_tstart` and `?_tend` rely on dashboard time parameters; for standalone Discover checks, use these examples and Discover's time picker instead of pasting unresolved parameters.

## Step 12: Configure Security Detection and Monitoring

**Evidence limitation:** The repository contains process-monitoring queries and screenshots, but no exported process execution detection rule, rule identifier, exact condition, schedule, or confirmed detection alert. Therefore the existing rule's precise configuration and successful alert execution are **unverified**. A process event or dashboard count is not itself a detection alert.

The intended process execution rule would identify selected execution activity in `logs-endpoint.events.process-*`. To verify an existing rule:

1. Open **Elastic Security > Rules** through navigation search, locate the process execution rule, and inspect its saved configuration.
2. Record its actual name, rule type, source/index pattern, hostname and process filters, schedule, look-back, exceptions, and enabled state privately. Confirm that its query matches the project's process source before treating it as part of this deployment.
3. If the rule is absent, treat creation as a new, unverified configuration. Select a supported rule type and a narrow lab test condition based on fields observed in Discover. The repository does not supply a production detection definition to import.
4. On the intended monitored host, generate a harmless process event:

```bash
hostname -f
```

This displays the host's fully qualified name and provides process activity for a collection check. It tests a detection rule only if that rule's actual condition matches this execution.

5. Confirm the resulting event in Discover with Step 11's process query. Match the host, command, and timestamp.
6. Wait for the rule's configured schedule and ingestion delay. Check rule execution status for errors, then open **Alerts** and filter for the rule, host, and test time.
7. Mark the detection test verified only after an alert is linked to the matching event and the rule execution is successful. If no alert appears, inspect the query conditions, timestamp field, permissions, schedule, exceptions, and alert time filter before concluding that detection failed.

No confirmed alert or automated response is claimed by this guide.

## Step 13: Configure Kibana Dashboards

In Kibana, open **Dashboards**, create or open the dashboard, add an ES|QL visualization, paste a **single** query from the appropriate directory, choose a visualization compatible with its output, and save the panel. Save the dashboard itself and verify that it can be reopened. Query definitions are present; exported saved dashboard objects are not included.

| Dashboard | Panels and query references | Screenshot evidence |
|---|---|---|
| **RHEL10 - Logstash1 Performance Monitoring** | Node health, CPU usage, current JVM heap and memory trends, pipeline events, throughput, and queue monitoring; [Logstash queries](../queries/logstash/) | Figures 6–12 |
| **RHEL10 Security Monitoring** | Process action distribution, execution trends, top processes, activity by user, recent processes, total events, and unique process names; [security queries](../queries/security/) | Figures 13–19 |
| **RHEL10 Authentication Monitoring** | Authentication outcomes and trends, successful/failed logins, failed attempts by user, recent authentication records, source IPs, privileged commands, and total events; [authentication queries](../queries/authentication/) | Figures 20–26 |

Use the dashboard time picker consistently. Confirm each panel returns data for its intended host and range before saving. Consult [dashboard documentation](dashboards.md) for the query/time-parameter conventions.

The captured Node1 values of **7,731 process events** and **734 unique processes**, as well as authentication percentages and totals, are historical observations. Zero pipeline throughput or a clear queue can reflect idle operation rather than an error. Reopening the saved dashboards and confirming current access still requires a live check.

## Step 14: Troubleshooting

### Elastic Agent not reporting Healthy

Compare Fleet's last check-in, assigned policy revision, and component errors with the Agent status commands in Step 4. Check the guest clock, DNS, routes, and outbound HTTPS access to the project-provided destinations. Inspect service messages:

```bash
sudo journalctl -u elastic-agent -n 100 --no-pager
```

Shows recent Agent service diagnostics. Look for connectivity, certificate, enrollment, or component failures. Review and sanitize output before sharing it.

```bash
timedatectl
```

Checks time and synchronization status. Clock errors can affect TLS, check-ins, and event time ranges.

### Missing Logstash metrics

Confirm the local API responds using Step 9. Check that the Logstash integration is assigned to Logstash1, Metrics (Elastic Agent) is enabled, and the integration target points to this host's API. Check integration component errors and the metrics query in Step 11. Application logs arriving successfully do not guarantee metric collection is working.

### Logstash service startup failures

```bash
sudo journalctl -u logstash -n 100 --no-pager
```

Shows startup failures reported by systemd. Combine this with the application log check in Step 9. Check configuration syntax, file permissions, disk space, port conflicts, and the service's pipeline selection. Stop the service before repeating Step 8's configuration test; do not run a second production process against its data directory.

### TCP port 5055 not listening

Use Step 9's listener check. Confirm the service has finished starting, the named pipeline loaded, and the configuration binds to `127.0.0.1`. If another process owns the port, identify it before changing anything. Testing from Node1 will not reach Logstash1's loopback input.

### JSON test events not appearing locally

Repeat Step 8's synthetic event only after confirming the listener. Review application logs for JSON parse or output permission errors and verify the output directory:

```bash
sudo ls -ld /var/lib/logstash/lab
```

Checks ownership and access permissions. Expect the service account to be able to write there.

```bash
sudo -u logstash test -w /var/lib/logstash/lab
```

Checks directory writability as Logstash. Exit status zero indicates writable; a silent result alone is not proof unless the exit status is checked. If an output file already exists, verify its ownership and permissions too.

```bash
sudo ls -l /var/lib/logstash/lab/events.jsonl
```

Checks whether the output file exists and shows its ownership and size. A missing file before any successful event is not sufficient to diagnose a failed installation.

```bash
sudo ausearch -m AVC -ts recent
```

When audit tools are installed, checks recent SELinux access denials. Investigate the specific denial and use an appropriate policy or file-context correction; do not disable SELinux as a shortcut.

### Missing authentication events

Check the System integration's authentication input and configured paths. Verify which logging service and files are actually present on this RHEL guest rather than assuming every installation writes the same files.

```bash
sudo journalctl -u sshd -n 50 --no-pager
```

Checks recent SSH service messages locally. These are local diagnostics; journal entries do not prove the configured integration has ingested them.

```bash
sudo ls -l /var/log/secure
```

Checks a common RHEL authentication log path. If absent, investigate the guest's logging configuration and the integration's supported inputs. Do not assume a nonexistent file is being collected.

Use an authorized normal login to generate activity, allow collection time, then run the authentication query. Do not create repeated failed privileged logins merely to populate a chart.

### ES|QL queries returning no results

Start with Step 11's broad queries. Confirm the source pattern exists, the host filter matches the observed `host.name`, and your account can read the data. Separate query syntax errors from empty result sets. Remove dashboard-only time parameters for Discover checks and review ingestion delays and the timestamp field.

### Dashboard data missing in the selected range

Widen the time range to include known captured or recent events, refresh, and check timezone differences. Compare a failing panel's query in Discover with the same host and time window. Ensure dashboard parameters are defined and the panel is saved. Historical screenshots do not guarantee that retained data still covers their original dates.

## Step 15: Deployment Verification

Use this checklist for a new deployment. Statuses reflect the repository's current evidence; unchecked boxes require a fresh operational check. **Verified** entries still need rechecking after installation, cloning, upgrades, or policy changes.

| Check | Evidence status | Acceptance criteria and remaining work |
|---|---|---|
| [ ] RHEL 10 virtual machines configured | **Verified** at documentation level; exact VM allocations **unverified** | Both guests boot; record actual OS releases and resources |
| [ ] Hostnames and network settings verified | Hostnames **verified** in evidence; full network plan **unverified** | Distinct hostnames, machine/Agent identities, addresses, working DNS and outbound access |
| [ ] Elastic Agent 9.5.5 installed | **Verified** in documentation and Logstash1 agent evidence | Recheck service, components, version, and boot enablement on both guests |
| [ ] Fleet enrollment and health confirmed | Logstash1 Healthy **verified** in Figure 1; current health of both guests **unverified** | Distinct Agent records, recent check-ins, correct policies, healthy components |
| [ ] System integration collecting data | Authentication collection **verified** in Figures 20–26; complete system metric coverage **unverified** | Confirm required logs and performance metrics for each intended host |
| [ ] Elastic Defend collecting endpoint events | **Verified** in Figures 4 and 13–19 | Confirm recent process events and endpoint policy status; prevention behavior remains separate |
| [ ] Logstash 9.5.5 installed and running | **Verified** by documentation and historical health evidence | Recheck version, service, API, and pipeline startup |
| [ ] Logstash monitoring metrics verified | **Verified** in Figures 2 and 6–12 | Confirm fresh metrics and application logs from Logstash1 |
| [ ] JSON pipeline tested locally | Configuration **verified**; end-to-end test **unverified** | Send a synthetic event and find it in the local JSON Lines file |
| [ ] Kibana dashboards created and accessible | Dashboard panels **verified** in screenshots; current saved access **unverified** | Save and reopen all three dashboards with working queries |
| [ ] Authentication monitoring verified | **Verified** in Figures 20–26 | Confirm new authorized login activity in the expected data source |
| [ ] Detection rules tested | **Unverified** | Inspect the actual rule, generate matching benign activity, and confirm execution plus a related alert |
| [ ] Optional cloud integrations and custom forwarding verified | **Planned/optional** | Keep outside deployment-complete claims until configured and independently tested |

## Step 16: Optional and Planned Integrations

| Integration | Scope and required verification |
|---|---|
| Microsoft 365 | **Planned/optional.** No operational connection or ingested Microsoft 365 events are demonstrated. Requires separately authorized access, integration configuration, and source-event verification. |
| Azure | **Planned/optional.** Azure-related components in the architecture do not prove an Azure activity integration. Cloud hosting location is distinct from collecting Azure tenant activity. Verify permissions, collection, and searchable events independently. |
| Custom Logstash-to-Elasticsearch forwarding | **Planned/unverified.** The sample pipeline has a file output only. A future Elasticsearch output requires separately secured authentication, a suitable Serverless destination, tested output configuration, and proof that a synthetic custom event arrived. |

Do not add active cloud credentials or connection strings to example configurations. The Logstash monitoring integration sending its own metrics/logs is not evidence that custom pipeline output reaches Elasticsearch.

## Step 17: Related Documentation

- [Architecture](architecture.md)
- [Dashboards and visualization notes](dashboards.md)
- [Figure captions and evidence index](figure-captions.md)
- [Screenshot gallery](figure-gallery.md)
- [ES|QL query collection](../queries/)
- [Original screenshots and captioned versions](../assets/screenshots/)
- [Safe local Logstash example](../examples/logstash/46-local-test.conf.example)
- [Security publication checklist](security-publication-checklist.md)

Review the publication checklist before sharing diagnostic output or preparing a public commit. No credentials or enrollment-token installation commands are needed in the public guide.
