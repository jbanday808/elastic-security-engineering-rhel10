# Figure gallery

Point-in-time snapshots from the RHEL 10 Elastic Security lab. All captions are descriptions of the captured screens, not current live status. Figures 1–26 include their captions inside the image; alternative text provides the same descriptions for accessibility.

## Architecture

### Figure 0: 00 Elastic Home Lab Architecture
![Figure 0](../assets/architecture/00_Elastic_Home_Lab_Architecture.png)
Overview of how RHEL 10 servers, Elastic Agent, Logstash, Elastic Cloud, and Kibana work together to collect and monitor security information.

## Elastic Agent and Logstash Integration

## Elastic Agent and Logstash Integration

**Figure 1:** Verifies the successful installation and health of the new Elastic Agent on Logstash1.

**Figure 2:** Verifies Logstash health, performance, and pipeline data collection in Elastic Security.

**Figure 3:** Verifies successful collection of Logstash application logs in Elastic Security.

**Figure 4:** Confirms Logstash1 process activity is successfully captured in Elastic Security.

**Figure 5:** Configures Logstash1 to monitor system logs and performance.

## RHEL10 - Logstash1 Performance Monitoring

**Figure 6:** Confirms Logstash1 is healthy and displays its system performance in Kibana.

**Figure 7:** Confirms Logstash1 is using 38% of its allocated memory.

**Figure 8:** Displays Logstash1 CPU activity over time, showing minimal resource usage.

**Figure 9:** Displays Logstash1 pipeline activity, showing no events received or processed.

**Figure 10:** Displays Logstash1 memory usage over time, showing stable performance.

**Figure 11:** Confirms Logstash1 recorded no event processing activity during the last 24 hours.

**Figure 12:** Confirms the Logstash1 processing queue is clear, with no events waiting.

## RHEL10 Security Monitoring

**Figure 13:** Displays the distribution of system activities monitored by Elastic Security.

**Figure 14:** Displays changes in system process activity over time in Elastic Security.

**Figure 15:** Highlights the 10 most frequently executed system processes monitored by Elastic Security.

**Figure 16:** Shows system activity by user, highlighting accounts with the most process executions.

**Figure 17:** Displays recent system activities, including user accounts, executed commands, and event details.

**Figure 18:** Confirms Elastic Security recorded 7,731 process events on Node1 in the last 24 hours.

**Figure 19:** Confirms Elastic Security recorded 734 unique processes on Node1 in the last 24 hours.

## RHEL10 Authentication Monitoring

**Figure 20:** Shows authentication results, with 95.7% of events classified as unknown.

**Figure 21:** Compares successful and failed login attempts recorded over the last seven days.

**Figure 22:** Highlights failed login attempts by user, with 9 for jbanday and 4 for root over the last seven days.

**Figure 23:** Displays recent successful and failed login attempts recorded in Elastic Security.

**Figure 24:** Displays administrative commands executed by privileged users across monitored RHEL 10 systems.

**Figure 25:** Identifies IP address 172.25.250.11 as the source of two authentication events in the last 24 hours.

**Figure 26:** Confirms Elastic Security recorded 4 authentication events in the last 24 hours.
