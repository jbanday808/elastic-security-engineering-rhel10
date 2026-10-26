# Figure gallery

Point-in-time screenshots from the RHEL 10 Elastic Security lab. Each screenshot is followed by its explanation; the values shown reflect the time of capture, not live system status.

## Architecture

![Figure 0: Overview of how RHEL 10 servers, Elastic Agent, Logstash, Elastic Cloud, and Kibana work together to collect and monitor security information.](../assets/architecture/00_Elastic_Home_Lab_Architecture.png)

**Figure 0:** Overview of how RHEL 10 servers, Elastic Agent, Logstash, Elastic Cloud, and Kibana work together to collect and monitor security information.

## Elastic Agent and Logstash Integration

![Figure 1: Verifies the successful installation and health of the new Elastic Agent on Logstash1.](../assets/screenshots/01_Elastic_Agent_Setup_Logstash1.png)

**Figure 1:** Verifies the successful installation and health of the new Elastic Agent on Logstash1.

![Figure 2: Verifies Logstash health, performance, and pipeline data collection in Elastic Security.](../assets/screenshots/02_Logstash_Metrics_Verification.png)

**Figure 2:** Verifies Logstash health, performance, and pipeline data collection in Elastic Security.

![Figure 3: Verifies successful collection of Logstash application logs in Elastic Security.](../assets/screenshots/03_Logstash_Logs_Verification.png)

**Figure 3:** Verifies successful collection of Logstash application logs in Elastic Security.

![Figure 4: Confirms Logstash1 process activity is successfully captured in Elastic Security.](../assets/screenshots/04_Logstash1_Process_Events.png)

**Figure 4:** Confirms Logstash1 process activity is successfully captured in Elastic Security.

![Figure 5: Configures Logstash1 to monitor system logs and performance.](../assets/screenshots/05_Logstash1_Integration_Settings.png)

**Figure 5:** Configures Logstash1 to monitor system logs and performance.

## RHEL10 - Logstash1 Performance Monitoring

![Figure 6: Confirms Logstash1 is healthy and displays its system performance in Kibana.](../assets/screenshots/06_Logstash1_Health_Performance.png)

**Figure 6:** Confirms Logstash1 is healthy and displays its system performance in Kibana.

![Figure 7: Confirms Logstash1 is using 38% of its allocated memory.](../assets/screenshots/07_Logstash1_JVM_Memory_Usage.png)

**Figure 7:** Confirms Logstash1 is using 38% of its allocated memory.

![Figure 8: Displays Logstash1 CPU activity over time, showing minimal resource usage.](../assets/screenshots/08_Logstash1_CPU_Usage_Trends.png)

**Figure 8:** Displays Logstash1 CPU activity over time, showing minimal resource usage.

![Figure 9: Displays Logstash1 pipeline activity, showing no events received or processed.](../assets/screenshots/09_Logstash1_Pipeline_Events.png)

**Figure 9:** Displays Logstash1 pipeline activity, showing no events received or processed.

![Figure 10: Displays Logstash1 memory usage over time, showing stable performance.](../assets/screenshots/10_Logstash1_Memory_Usage_Trends.png)

**Figure 10:** Displays Logstash1 memory usage over time, showing stable performance.

![Figure 11: Confirms Logstash1 recorded no event processing activity during the last 24 hours.](../assets/screenshots/11_Logstash1_Pipeline_Throughput.png)

**Figure 11:** Confirms Logstash1 recorded no event processing activity during the last 24 hours.

![Figure 12: Confirms the Logstash1 processing queue is clear, with no events waiting.](../assets/screenshots/12_Logstash1_Pipeline_Queue.png)

**Figure 12:** Confirms the Logstash1 processing queue is clear, with no events waiting.

## RHEL10 Security Monitoring

![Figure 13: Displays the distribution of system activities monitored by Elastic Security.](../assets/screenshots/13_Process_Action_Distribution.png)

**Figure 13:** Displays the distribution of system activities monitored by Elastic Security.

![Figure 14: Displays changes in system process activity over time in Elastic Security.](../assets/screenshots/14_Process_Execution_Trends.png)

**Figure 14:** Displays changes in system process activity over time in Elastic Security.

![Figure 15: Highlights the 10 most frequently executed system processes monitored by Elastic Security.](../assets/screenshots/15_Top_10_Process_Executions.png)

**Figure 15:** Highlights the 10 most frequently executed system processes monitored by Elastic Security.

![Figure 16: Shows system activity by user, highlighting accounts with the most process executions.](../assets/screenshots/16_Process_Executions_By_User.png)

**Figure 16:** Shows system activity by user, highlighting accounts with the most process executions.

![Figure 17: Displays recent system activities, including user accounts, executed commands, and event details.](../assets/screenshots/17_Recent_Process_Activity.png)

**Figure 17:** Displays recent system activities, including user accounts, executed commands, and event details.

![Figure 18: Confirms Elastic Security recorded 7,731 process events on Node1 in the last 24 hours.](../assets/screenshots/18_Node1_Total_Process_Events.png)

**Figure 18:** Confirms Elastic Security recorded 7,731 process events on Node1 in the last 24 hours.

![Figure 19: Confirms Elastic Security recorded 734 unique processes on Node1 in the last 24 hours.](../assets/screenshots/19_Node1_Unique_Processes.png)

**Figure 19:** Confirms Elastic Security recorded 734 unique processes on Node1 in the last 24 hours.

## RHEL10 Authentication Monitoring

![Figure 20: Shows authentication results, with 95.7% of events classified as unknown.](../assets/screenshots/20_Authentication_Outcome_Distribution.png)

**Figure 20:** Shows authentication results, with 95.7% of events classified as unknown.

![Figure 21: Compares successful and failed login attempts recorded over the last seven days.](../assets/screenshots/21_Authentication_Success_Failure.png)

**Figure 21:** Compares successful and failed login attempts recorded over the last seven days.

![Figure 22: Highlights failed login attempts by user, with 9 for jbanday and 4 for root over the last seven days.](../assets/screenshots/22_Failed_Authentication_By_User.png)

**Figure 22:** Highlights failed login attempts by user, with 9 for jbanday and 4 for root over the last seven days.

![Figure 23: Displays recent successful and failed login attempts recorded in Elastic Security.](../assets/screenshots/23_Recent_Authentication_Activity.png)

**Figure 23:** Displays recent successful and failed login attempts recorded in Elastic Security.

![Figure 24: Displays administrative commands executed by privileged users across monitored RHEL 10 systems.](../assets/screenshots/24_Privileged_Command_Activity.png)

**Figure 24:** Displays administrative commands executed by privileged users across monitored RHEL 10 systems.

![Figure 25: Identifies IP address 172.25.250.11 as the source of two authentication events in the last 24 hours.](../assets/screenshots/25_Authentication_Source_IPs.png)

**Figure 25:** Identifies IP address 172.25.250.11 as the source of two authentication events in the last 24 hours.

![Figure 26: Confirms Elastic Security recorded 4 authentication events in the last 24 hours.](../assets/screenshots/26_Total_Authentication_Events.png)

**Figure 26:** Confirms Elastic Security recorded 4 authentication events in the last 24 hours.
