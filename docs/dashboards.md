# Dashboard documentation

## RHEL10 - Logstash1 Performance Monitoring

Node health, JVM heap usage, CPU trends, pipeline event totals, queue status, and throughput. Pipeline rates shown as zero in some captured windows; this is consistent with a period of little or no incoming data, not proof of a broken pipeline.

## RHEL10 Security Monitoring

Node1 endpoint activity includes process action distribution, process execution trends, top process names, activity by user, total events, unique process names, and recent process records. Figures 18–19 describe captured 24-hour values of 7,731 events and 734 unique processes; these are historical screenshot observations.

## RHEL10 Authentication Monitoring

System authentication log events include outcomes, failed attempts, source IPs where available, privileged commands, and recent login details. Many local authentication records have no source IP or are uncategorized. Figures 20–26 document a specific snapshot, not continuous results.

## Reproducing charts

Open Kibana > Dashboards > Create visualization (query). Paste a **single** `.esql` file from `queries/` into the ES|QL editor, set the dashboard time filter, select the visual type, and save the panel. Dashboard-only time variables `?_tstart` and `?_tend` may not work in a standalone Discover session; use Discover's time picker for exploratory queries.

---

# ES|QL Query Reference: Line-by-Line Explanations

This reference explains every query in plain language. **Each numbered explanation corresponds to the same line number in the linked `.esql` source file.** Some commands continue onto the next line; read the lines together when needed.

ES|QL helps analysts find and summarize security and performance records. In these queries, `FROM` selects data, `WHERE` filters it, `STATS` counts or summarizes it, `SORT` puts it in order, and `LIMIT` caps the displayed results. The `?_tstart` and `?_tend` values represent the selected time range.

The explanations describe what the queries are designed to do, not a live reading or confirmation that suspicious activity occurred.

## Authentication Monitoring

### [`authentication-events-trend.esql`](../queries/authentication/authentication-events-trend.esql)

**Purpose:** Tracks authentication activity every 30 minutes to identify unusual changes.

| Line | Explanation |
|---:|---|
| 1 | Retrieves system authentication records. |
| 2 | Selects records between the dashboard's start and end times. |
| 3 | Includes only records categorized as authentication events. |
| 4 | Counts the matching authentication events. |
| 5 | Groups those counts into 30-minute time intervals. |
| 6 | Lists the intervals from earliest to latest. |

**Summary:** Shows how authentication activity rises or falls over the selected period.

### [`failed-auth-by-user.esql`](../queries/authentication/failed-auth-by-user.esql)

**Purpose:** Finds accounts with the most failed authentication attempts.

| Line | Explanation |
|---:|---|
| 1 | Opens the system authentication records. |
| 2 | Starts the search at the chosen beginning time. |
| 3 | Stops the search at the chosen ending time. |
| 4 | Selects only records marked as failures. |
| 5 | Counts failures for each username, using **Unknown** when no username is recorded. |
| 6 | Places the accounts with the most failures first. |
| 7 | Shows up to 10 accounts. |

**Summary:** Highlights accounts with repeated authentication failures for further review.

### [`login-outcomes.esql`](../queries/authentication/login-outcomes.esql)

**Purpose:** Compares the recorded results of authentication activity.

| Line | Explanation |
|---:|---|
| 1 | Retrieves the authentication records. |
| 2 | Limits the search to the selected time period. |
| 3 | Includes only records that have a recorded outcome. |
| 4 | Counts records separately for each outcome, such as success or failure. |
| 5 | Displays the most common outcomes first. |

**Summary:** Shows how often each recorded authentication outcome occurred.

### [`outcome-distribution.esql`](../queries/authentication/outcome-distribution.esql)

**Purpose:** Shows the distribution of authentication outcomes, including missing classifications.

| Line | Explanation |
|---:|---|
| 1 | Retrieves the authentication records. |
| 2 | Selects records within the chosen time period. |
| 3 | Counts the matching records. |
| 4 | Groups records by outcome and uses **unknown** when an outcome is missing. |
| 5 | Shows the most frequent outcome groups first. |

**Summary:** Helps identify the proportions of successful, failed, and unknown outcomes.

### [`recent-auth-events.esql`](../queries/authentication/recent-auth-events.esql)

**Purpose:** Displays recent authentication events for investigation.

| Line | Explanation |
|---:|---|
| 1 | Retrieves system authentication records. |
| 2 | Starts the search at the chosen beginning time. |
| 3 | Stops the search at the chosen ending time. |
| 4 | Includes records categorized as authentication. |
| 5 | Places the newest events first. |
| 6 | Limits the display to 100 events. |
| 7 | Shows the time, computer, username, activity, outcome, source IP address, and message. |

**Summary:** Shows who was involved in recent authentication activity and what was recorded.

### [`sudo-activity.esql`](../queries/authentication/sudo-activity.esql)

**Purpose:** Reviews commands run with elevated administrative permissions.

| Line | Explanation |
|---:|---|
| 1 | Retrieves system authentication records. |
| 2 | Selects records within the chosen period. |
| 3 | Includes only records with a logged `sudo` command. |
| 4 | Places the newest command records first. |
| 5 | Shows up to 50 records. |
| 6 | Retains the time, computer, executing user, and target user. |
| 7 | Also retains the command, terminal, and original message. |
| 8 | Renames the executing-user field to `executed_by`. |
| 9 | Renames the target-user field to `target_user`. |
| 10 | Renames the administrative-command field to `sudo_command`. |
| 11 | Renames the terminal field to `terminal`. |

**Summary:** Helps determine which accounts ran recorded administrative commands.

### [`top-source-ips.esql`](../queries/authentication/top-source-ips.esql)

**Purpose:** Identifies IP addresses associated with the most authentication events.

| Line | Explanation |
|---:|---|
| 1 | Retrieves system authentication records. |
| 2 | Begins at the selected start time. |
| 3 | Ends at the selected end time. |
| 4 | Includes only records containing a source IP address. |
| 5 | Counts events for each source IP address. |
| 6 | Lists the IP addresses with the most events first. |
| 7 | Displays up to 10 IP addresses. |

**Summary:** Helps analysts identify the recorded origins of authentication activity.

### [`total-authentication-events.esql`](../queries/authentication/total-authentication-events.esql)

**Purpose:** Counts authentication events in the selected period.

| Line | Explanation |
|---:|---|
| 1 | Retrieves system authentication records. |
| 2 | Filters to the selected time period. |
| 3 | Includes only records categorized as authentication. |
| 4 | Counts all matching events. |

**Summary:** Gives a single total for recorded authentication activity.

## Logstash Performance Monitoring

### [`cpu-usage-trend.esql`](../queries/logstash/cpu-usage-trend.esql)

**Purpose:** Tracks Logstash1 CPU usage over time.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash node performance measurements. |
| 2 | Filters measurements to the Logstash1 server. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Calculates average CPU usage. |
| 6 | Groups measurements into 30-minute intervals. |
| 7 | Displays the intervals from earliest to latest. |

**Summary:** Shows how Logstash CPU usage changes over time.

### [`jvm-heap-current.esql`](../queries/logstash/jvm-heap-current.esql)

**Purpose:** Displays the latest recorded Logstash Java memory usage.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash node measurements. |
| 2 | Filters measurements to Logstash1. |
| 3 | Limits results to the selected period. |
| 4 | Places the newest measurement first. |
| 5 | Chooses only that most recent measurement. |
| 6 | Converts the Java memory-use percentage into a numeric value. |
| 7 | Displays only the memory-use percentage. |

**Summary:** Shows the latest recorded share of the Java memory allocation being used.

### [`jvm-memory-trend.esql`](../queries/logstash/jvm-memory-trend.esql)

**Purpose:** Tracks Logstash Java memory usage over time.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash node measurements. |
| 2 | Selects the Logstash1 server. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Calculates average Java memory usage and rounds it to one decimal place. |
| 6 | Groups results into 30-minute intervals. |
| 7 | Arranges those intervals from earliest to latest. |

**Summary:** Helps identify changes in Logstash memory usage.

### [`logstash-health.esql`](../queries/logstash/logstash-health.esql)

**Purpose:** Summarizes Logstash1 health and resource usage.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash node health and performance records. |
| 2 | Filters records to Logstash1. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Places the newest health record first. |
| 6 | Chooses the latest available record. |
| 7 | Converts uptime into hours and rounds it to one decimal place. |
| 8 | Labels the reported Logstash status as `node_health`. |
| 9 | Labels the software version as `version`. |
| 10 | Labels Java memory usage as `heap_pct`. |
| 11 | Labels CPU usage as `cpu_pct`. |
| 12 | Labels the record time as `last_seen`. |
| 13 | Displays only the host, health, version, memory, CPU, uptime, and latest-record time. |

**Summary:** Provides a snapshot of the server's most recently reported condition.

### [`metrics-datasets.esql`](../queries/logstash/metrics-datasets.esql)

**Purpose:** Shows which Logstash monitoring data types are available.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash monitoring records from all matching datasets. |
| 2 | Counts records for each data type and server. |
| 3 | Lists data types with the most records first. |

**Summary:** Shows which servers and monitoring categories are contributing records.

### [`pipeline-events.esql`](../queries/logstash/pipeline-events.esql)

**Purpose:** Reports the latest event counters for each Logstash pipeline.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash pipeline measurements. |
| 2 | Filters the results to Logstash1. |
| 3 | Limits the measurements to the selected period. |
| 4 | Includes records with a pipeline name. |
| 5 | Converts the incoming-event counter to a whole number. |
| 6 | Converts the outgoing-event counter to a whole number. |
| 7 | Retrieves the latest incoming-event counter. |
| 8 | Retrieves the latest outgoing-event counter. |
| 9 | Records the time of the latest measurement. |
| 10 | Groups results by pipeline name. |
| 11 | Lists the pipelines alphabetically. |

**Summary:** Shows the latest recorded cumulative incoming and outgoing event counts; these are not necessarily counts for just the selected period.

### [`pipeline-queue.esql`](../queries/logstash/pipeline-queue.esql)

**Purpose:** Checks whether Logstash has events waiting in its pipelines.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash pipeline measurements. |
| 2 | Filters measurements to Logstash1. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Converts the queued-event count into a whole number. |
| 6 | Retrieves the latest queued-event count. |
| 7 | Retrieves the most recently recorded queue type. |
| 8 | Records when the latest measurement was captured. |
| 9 | Groups results by pipeline name. |
| 10 | Lists the pipelines alphabetically. |

**Summary:** Helps identify events waiting to be processed.

### [`pipeline-throughput.esql`](../queries/logstash/pipeline-throughput.esql)

**Purpose:** Measures how quickly events enter and leave Logstash pipelines.

| Line | Explanation |
|---:|---|
| 1 | Retrieves pipeline performance measurements. |
| 2 | Filters measurements to Logstash1. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Calculates the average incoming-event rate. |
| 6 | Calculates the average outgoing-event rate. |
| 7 | Divides the selected time range into 48 intervals. |
| 8 | Excludes intervals missing both incoming and outgoing measurements. |
| 9 | Rounds the incoming rate to two decimal places. |
| 10 | Rounds the outgoing rate to two decimal places. |
| 11 | Displays intervals from earliest to latest. |

**Summary:** Shows changes in Logstash processing speed and may help reveal slowdowns.

### [`process-events-logstash1.esql`](../queries/logstash/process-events-logstash1.esql)

**Purpose:** Shows recent process activity on the Logstash1 server.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Selects records from the Logstash1 server. |
| 3 | Places the newest records first. |
| 4 | Displays up to 20 process events. |
| 5 | Shows the event time, server, username, program name, and recorded action. |

**Summary:** Helps review recently recorded program activity on Logstash1.

### [`recent-application-logs.esql`](../queries/logstash/recent-application-logs.esql)

**Purpose:** Displays recent Logstash application log messages.

| Line | Explanation |
|---:|---|
| 1 | Retrieves Logstash application logs. |
| 2 | Places the newest messages first. |
| 3 | Displays up to 20 log entries. |
| 4 | Shows the time, server name, and message. |

**Summary:** Helps investigate Logstash warnings, errors, and other application messages.

## RHEL 10 Security Monitoring

### [`process-actions-node1.esql`](../queries/security/process-actions-node1.esql)

**Purpose:** Shows the types of process events recorded on Node1.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Filters to the Node1 server. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Includes only events with a recorded action. |
| 6 | Counts events separately for each type of action. |
| 7 | Lists the most common actions first. |

**Summary:** Shows which process actions occur most frequently on Node1.

### [`process-events-by-user.esql`](../queries/security/process-events-by-user.esql)

**Purpose:** Identifies accounts with the most recorded process activity.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process records. |
| 2 | Filters to the Node1 server. |
| 3 | Limits records to the selected time period. |
| 4 | Includes only records containing a username. |
| 5 | Counts process events for each username. |
| 6 | Places the most active accounts first. |
| 7 | Displays up to 10 accounts. |

**Summary:** Shows which user accounts are associated with the most process events.

### [`process-execution-trend.esql`](../queries/security/process-execution-trend.esql)

**Purpose:** Tracks process events on Node1 over time.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Selects Node1. |
| 3 | Limits the results to the selected time period. |
| 4 | Counts process events. |
| 5 | Groups the counts into 30-minute intervals. |
| 6 | Orders the intervals from earliest to latest. |

**Summary:** Helps spot unusual increases or decreases in process activity.

### [`recent-processes-node1.esql`](../queries/security/recent-processes-node1.esql)

**Purpose:** Displays recent process activity on Node1.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Selects the Node1 server. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Places the newest activity first. |
| 6 | Displays up to 50 events. |
| 7 | Shows time, server, user, program, command details, and recorded action. |

**Summary:** Helps review recent programs, commands, and user activity.

### [`top-processes-node1.esql`](../queries/security/top-processes-node1.esql)

**Purpose:** Identifies frequently recorded programs on Node1.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Selects the Node1 server. |
| 3 | Begins at the selected start time. |
| 4 | Ends at the selected end time. |
| 5 | Includes records with a program name. |
| 6 | Counts events for each program name. |
| 7 | Places programs with the most events first. |
| 8 | Displays up to 10 program names. |

**Summary:** Highlights commonly observed programs and potential activity worth investigating.

### [`total-process-events.esql`](../queries/security/total-process-events.esql)

**Purpose:** Counts recorded process events on Node1.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Selects the Node1 server. |
| 3 | Limits records to the selected time period. |
| 4 | Counts all matching process events. |

**Summary:** Provides the overall recorded process-event count for the selected period.

### [`unique-processes.esql`](../queries/security/unique-processes.esql)

**Purpose:** Counts distinct program names observed on Node1.

| Line | Explanation |
|---:|---|
| 1 | Retrieves endpoint process activity records. |
| 2 | Selects the Node1 server. |
| 3 | Limits records to the selected time period. |
| 4 | Includes only records containing a program name. |
| 5 | Counts each different program name once. |

**Summary:** Shows how many different process names were recorded; it does not count every running process instance.

---

## How to use these queries

Open **Kibana → Dashboard → Create visualization (query)**, then copy one query from the linked `queries/` file into the ES|QL editor. Select the appropriate dashboard time range and visualization. Some dashboard time parameters may need adjustment when running a query outside a dashboard. Review the results alongside the recorded timestamps and available context.

**Remember:** These are point-in-time lab examples. High counts, missing source addresses, or unknown outcomes can be investigation leads but do not automatically prove an attack.
