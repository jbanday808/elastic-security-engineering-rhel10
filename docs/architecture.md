# Elastic Home Lab Architecture

![Figure 0: Elastic Home Lab Architecture](../assets/architecture/00_Elastic_Home_Lab_Architecture.png)

**Figure 0: Elastic Security Home Lab Architecture**

## Overview

The lab uses two RHEL 10 virtual machines, `node1` and `logstash1`. Elastic Agent collects system logs and metrics, Elastic Defend monitors endpoint activity, and the Logstash integration collects Logstash logs and monitoring metrics. Elastic Cloud hosts the data collection, search, and security investigation tools, with Kibana providing dashboards and investigation views.

The included sample Logstash pipeline writes locally. It does not establish that custom Logstash events were forwarded to Elasticsearch. Cloud integrations shown in the diagram are illustrative or optional unless independently verified.

## Step-by-Step Architecture Explanation

### Step 1: Data Sources — RHEL 10 Servers

The lab begins with two Red Hat Enterprise Linux 10 virtual machines: `node1` and `logstash1`. These servers generate records of system behavior, running programs, user logins, and administrative commands. Node1 supplies endpoint security activity, while Logstash1 also provides logs and performance information about Logstash.

### Step 2: Elastic Agent — Data Collection

Elastic Agent 9.5.5 runs on the monitored servers and collects the information selected through its integrations. Fleet in Elastic Cloud centrally manages the agents and their policies. Agent health checks help confirm that the collection software is running; the screenshots document its status at the time of capture.

### Step 3: System Integration — Server Monitoring

The System integration collects operating system logs and performance metrics. This information helps explain server resource usage and authentication activity, including successful and failed logins. The authentication dashboard presents recorded login outcomes, usernames, source addresses where available, and privileged command activity.

### Step 4: Elastic Defend — Endpoint Protection

Elastic Defend provides endpoint security monitoring through Elastic Agent. The project demonstrates visibility into process activity, including executed programs, process actions, and associated users. These records help an investigator understand what ran on a monitored server. The screenshots demonstrate collected activity; they do not independently verify every prevention capability or automated response action.

### Step 5: Logstash — Data Processing

Logstash runs on `logstash1` and provides a pipeline for receiving and processing data. The included sample pipeline accepts JSON input on loopback TCP port `5055` and writes the resulting events to a local file. This demonstrates local processing only; forwarding these custom events to Elasticsearch is not implemented by the sample configuration.

Separately, the Logstash integration collects application logs and monitoring metrics for Elastic Cloud. The performance dashboard displays node health, CPU use, JVM memory, pipeline event counts, throughput, and queue information. Collecting these monitoring records is distinct from forwarding the sample pipeline's output.

### Step 6: Microsoft 365 — Cloud Activity Monitoring

Microsoft 365 represents a planned or optional cloud data source in the architecture. A configured integration could add cloud activity records to support investigation alongside server events. This project does not verify an operational Microsoft 365 connection or collected Microsoft 365 events, so the diagram should not be read as evidence that this integration is deployed.

### Step 7: Elastic Cloud — Centralized Security Platform

Elastic Cloud hosts the lab's managed data collection, search, and security investigation tools. It brings together the system, endpoint, and Logstash monitoring data collected by the configured agents and integrations. This gives the investigator a central place to review activity from the monitored servers. Optional sources require separate configuration and verification before they can be included in that view.

### Step 8: Elasticsearch — Data Storage and Analysis

Elasticsearch provides the storage and search capabilities used to analyze the collected records. Queries can filter activity by host, user, time, or event type and calculate totals or trends. The project includes queries for Logstash monitoring, process activity, and authentication records. These records arrive through the configured collection paths; the local sample Logstash pipeline does not establish an Elasticsearch output path.

### Step 9: Kibana — Security Dashboards and Visualization

Kibana provides the visual interface for exploring records and reviewing dashboards. The lab organizes its evidence into Logstash performance, endpoint security, and authentication monitoring. Charts and tables make resource use, frequently executed programs, login outcomes, and recent activity easier to understand. Screenshot values describe the captured time windows and should not be interpreted as current live readings.

### Step 10: Security Investigation and Response

An investigator can use the dashboards to identify activity that needs closer review, then inspect the underlying records in Kibana Discover. Comparing timestamps, hosts, users, executed commands, and login outcomes helps build a picture of what happened. Any response should follow verified findings and the lab's operating procedures. The documentation demonstrates investigation visibility; it does not establish that automated containment or remediation has been configured or tested.

## Summary

Figure 0 shows how the RHEL 10 servers, Elastic Agent, System integration, Elastic Defend, Logstash, and Elastic Cloud support the lab's security monitoring workflow. Agents and integrations collect system, endpoint, and Logstash monitoring records; Elasticsearch supports storage and analysis, and Kibana presents the results for investigation.

The implemented evidence covers server monitoring, process visibility, authentication activity, and Logstash health. The sample Logstash pipeline processes data locally and writes to a file. Elasticsearch forwarding from that pipeline, Microsoft 365 collection, other optional cloud connections, and automated response must be verified separately before they are described as operational. Together, the deployed components provide a practical foundation for learning centralized security monitoring and investigation.

## Related Documentation

See the [deployment guide](deployment.md) and [dashboard documentation](dashboards.md) for the existing implementation details.
