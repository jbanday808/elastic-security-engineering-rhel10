# RHEL 10 Elastic Security Home Lab

Hands-on Elastic Security project using **two Red Hat Enterprise Linux 10 virtual machines**, Elastic Agent, Elastic Defend, Logstash, Elasticsearch, and Kibana.

![Elastic home lab architecture](assets/architecture/00_Elastic_Home_Lab_Architecture.png)

## Architecture

Two RHEL 10 servers send system, endpoint security, and Logstash monitoring data through Elastic Agent to Elastic Cloud for investigation in Kibana. The sample Logstash pipeline demonstrates local processing.

See the [architecture overview](docs/architecture.md) for Figure 0 and the documented component roles.

## Purpose

Collect and monitor system logs, endpoint process events, authentication activity, and Logstash health information. Investigate activity through Kibana and demonstrate security monitoring with dashboards.

## Lab environment

| Component | Purpose |
|---|---|
| `node1.domain250.example.com` | RHEL 10 endpoint monitored with Elastic Agent and Elastic Defend |
| `logstash1.domain250.example.com` | RHEL 10 server running Logstash plus its own Elastic Agent |
| Elastic Cloud Security (serverless) | Hosts managed data collection, search, analysis, and security investigation tools |
| Kibana | Displays the dashboards and investigation results |
| Logstash local pipeline | Demonstrates JSON input on loopback TCP port 5055 and a local file output |

> **Scope note:** The sample Logstash pipeline included here writes locally. It does not prove that custom Logstash events were forwarded to Elasticsearch. The monitoring integration and Elastic Agent send separate monitoring/security data to Elastic Cloud. Cloud integrations shown in the architecture are illustrative or optional unless independently verified.

## Dashboards

1. **RHEL10 - Logstash1 Performance Monitoring** — CPU, JVM memory, Logstash node status, pipeline event counts, throughput, and queue information.
2. **RHEL10 Security Monitoring** — process events, process counts, frequently seen programs, process action distribution, and activity by user on Node1.
3. **RHEL10 Authentication Monitoring** — successful and failed logins, recent authentication records, source IPs where available, and recorded `sudo` commands.

## Evidence

All **27** project figures (Figure 0–26) are included. Browse the [visual figure gallery](docs/figure-gallery.md).

Captioned screenshots preserve the original screenshot pixels and append a white caption panel beneath each image. Browse by category:

- [Elastic Agent and Logstash Integration (Figures 1–5)](docs/figure-gallery.md#elastic-agent-and-logstash-integration)
- [RHEL10 - Logstash1 Performance Monitoring (Figures 6–12)](docs/figure-gallery.md#rhel10---logstash1-performance-monitoring)
- [RHEL10 Security Monitoring (Figures 13–19)](docs/figure-gallery.md#rhel10-security-monitoring)
- [RHEL10 Authentication Monitoring (Figures 20–26)](docs/figure-gallery.md#rhel10-authentication-monitoring)

![Logstash1 health and performance](assets/screenshots/captioned/06_Logstash1_Health_Performance.png)

See the [caption verification and security review](docs/caption-review.md) before publication.



- [Figures 0–26 and descriptions](docs/figure-captions.md)
- [Screenshot inventory](docs/SCREENSHOTS-TO-ADD.md)
- [Deployment summary](docs/deployment.md)
- [Dashboards and queries](docs/dashboards.md)
- [Publication checklist](docs/security-publication-checklist.md)

## Configuration and queries

- Local-only example Logstash pipeline: [`examples/logstash/46-local-test.conf.example`](examples/logstash/46-local-test.conf.example)
- Saved ES|QL examples: [`queries/`](queries/) (grouped into Logstash, security, and authentication)

## Documentation status

This repository provides **sanitized project documentation and representative evidence**. It intentionally excludes original Word documents, passwords, enrollment keys, Azure client secrets, and other private information. Screenshots show results captured during the lab, not live data.

## Verification

Run `bash scripts/verify-screenshots.sh` to check that all 27 numbered figures are available. To regenerate the 26 captioned images and verify pixel preservation, run `python3 scripts/caption-screenshots.py` (requires Pillow and DejaVu Sans).

## References

- [Elastic official documentation](https://www.elastic.co/docs)
- [Elastic Agent and Fleet](https://www.elastic.co/docs/reference/fleet)
- [Logstash reference](https://www.elastic.co/docs/reference/logstash)
- [VS Code with WSL](https://code.visualstudio.com/docs/remote/wsl)

## Publish to GitHub

Follow [WSL / VS Code / GitHub commands](docs/github-upload.md). Review [safe publication](docs/security-publication-checklist.md) first.
