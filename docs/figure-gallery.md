# Figure gallery

Point-in-time snapshots from the RHEL 10 Elastic Security lab. All captions are descriptions of the captured screens, not current live status. Figures 1–26 include their captions inside the image; alternative text provides the same descriptions for accessibility.

## Architecture

### Figure 0: 00 Elastic Home Lab Architecture
![Figure 0](../assets/architecture/00_Elastic_Home_Lab_Architecture.png)
Overview of how RHEL 10 servers, Elastic Agent, Logstash, Elastic Cloud, and Kibana work together to collect and monitor security information.

## Elastic Agent and Logstash Integration

![Figure 1: Verifies the successful installation and health of the new Elastic Agent on Logstash1.](../assets/screenshots/captioned/01_Elastic_Agent_Setup_Logstash1.png)

![Figure 2: Verifies Logstash health, performance, and pipeline data collection in Elastic Security.](../assets/screenshots/captioned/02_Logstash_Metrics_Verification.png)

![Figure 3: Verifies successful collection of Logstash application logs in Elastic Security.](../assets/screenshots/captioned/03_Logstash_Logs_Verification.png)

![Figure 4: Confirms Logstash1 process activity is successfully captured in Elastic Security.](../assets/screenshots/captioned/04_Logstash1_Process_Events.png)

![Figure 5: Configures Logstash1 to monitor system logs and performance.](../assets/screenshots/captioned/05_Logstash1_Integration_Settings.png)

## RHEL10 - Logstash1 Performance Monitoring

![Figure 6: Confirms Logstash1 is healthy and displays its system performance in Kibana.](../assets/screenshots/captioned/06_Logstash1_Health_Performance.png)

![Figure 7: Confirms Logstash1 is using 38% of its allocated memory.](../assets/screenshots/captioned/07_Logstash1_JVM_Memory_Usage.png)

![Figure 8: Displays Logstash1 CPU activity over time, showing minimal resource usage.](../assets/screenshots/captioned/08_Logstash1_CPU_Usage_Trends.png)

![Figure 9: Displays Logstash1 pipeline activity, showing no events received or processed.](../assets/screenshots/captioned/09_Logstash1_Pipeline_Events.png)

![Figure 10: Displays Logstash1 memory usage over time, showing stable performance.](../assets/screenshots/captioned/10_Logstash1_Memory_Usage_Trends.png)

![Figure 11: Confirms Logstash1 recorded no event processing activity during the last 24 hours.](../assets/screenshots/captioned/11_Logstash1_Pipeline_Throughput.png)

![Figure 12: Confirms the Logstash1 processing queue is clear, with no events waiting.](../assets/screenshots/captioned/12_Logstash1_Pipeline_Queue.png)

## RHEL10 Security Monitoring

![Figure 13: Displays the distribution of system activities monitored by Elastic Security.](../assets/screenshots/captioned/13_Process_Action_Distribution.png)

![Figure 14: Displays changes in system process activity over time in Elastic Security.](../assets/screenshots/captioned/14_Process_Execution_Trends.png)

![Figure 15: Highlights the 10 most frequently executed system processes monitored by Elastic Security.](../assets/screenshots/captioned/15_Top_10_Process_Executions.png)

![Figure 16: Shows system activity by user, highlighting accounts with the most process executions.](../assets/screenshots/captioned/16_Process_Executions_By_User.png)

![Figure 17: Displays recent system activities, including user accounts, executed commands, and event details.](../assets/screenshots/captioned/17_Recent_Process_Activity.png)

![Figure 18: Confirms Elastic Security recorded 7,731 process events on Node1 in the last 24 hours.](../assets/screenshots/captioned/18_Node1_Total_Process_Events.png)

![Figure 19: Confirms Elastic Security recorded 734 unique processes on Node1 in the last 24 hours.](../assets/screenshots/captioned/19_Node1_Unique_Processes.png)

## RHEL10 Authentication Monitoring

![Figure 20: Shows authentication results, with 95.7% of events classified as unknown.](../assets/screenshots/captioned/20_Authentication_Outcome_Distribution.png)

![Figure 21: Compares successful and failed login attempts recorded over the last seven days.](../assets/screenshots/captioned/21_Authentication_Success_Failure.png)

![Figure 22: Highlights failed login attempts by user, with 9 for jbanday and 4 for root over the last seven days.](../assets/screenshots/captioned/22_Failed_Authentication_By_User.png)

![Figure 23: Displays recent successful and failed login attempts recorded in Elastic Security.](../assets/screenshots/captioned/23_Recent_Authentication_Activity.png)

![Figure 24: Displays administrative commands executed by privileged users across monitored RHEL 10 systems.](../assets/screenshots/captioned/24_Privileged_Command_Activity.png)

![Figure 25: Identifies IP address 172.25.250.11 as the source of two authentication events in the last 24 hours.](../assets/screenshots/captioned/25_Authentication_Source_IPs.png)

![Figure 26: Confirms Elastic Security recorded 4 authentication events in the last 24 hours.](../assets/screenshots/captioned/26_Total_Authentication_Events.png)
