# Dashboard documentation

## RHEL10 - Logstash1 Performance Monitoring

Node health, JVM heap usage, CPU trends, pipeline event totals, queue status, and throughput. Pipeline rates shown as zero in some captured windows; this is consistent with a period of little or no incoming data, not proof of a broken pipeline.

## RHEL10 Security Monitoring

Node1 endpoint activity includes process action distribution, process execution trends, top process names, activity by user, total events, unique process names, and recent process records. Figures 18–19 describe captured 24-hour values of 7,731 events and 734 unique processes; these are historical screenshot observations.

## RHEL10 Authentication Monitoring

System authentication log events include outcomes, failed attempts, source IPs where available, privileged commands, and recent login details. Many local authentication records have no source IP or are uncategorized. Figures 20–26 document a specific snapshot, not continuous results.

## Reproducing charts

Open Kibana > Dashboards > Create visualization (query). Paste a **single** `.esql` file from `queries/` into the ES|QL editor, set the dashboard time filter, select the visual type, and save the panel. Dashboard-only time variables `?_tstart` and `?_tend` may not work in a standalone Discover session; use Discover's time picker for exploratory queries.
