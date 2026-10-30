# Cyber Range IDS & SOC Dashboard

A local-first educational cyber range that connects short Red Team simulations, Blue Team event analysis, SQLite alert storage and a Flask SOC dashboard.

> **Scope:** use only private IPv4 lab systems that you own or are explicitly authorised to test. The brute-force, web and DDoS scenarios are offline demonstrations. The IPS module records a simulated decision; it does not change operating-system firewall rules.

## Current features

- **Red Team scenarios:** fixed-port TCP checks against private IPv4 lab addresses; offline brute-force, web-attack indicator and DDoS traffic-pattern demonstrations.
- **Blue Team classification:** maps IDS signature text into Port Scan, Brute Force, Web Attack, DDoS or Unknown categories and severity.
- **Suricata EVE import:** manually imports alert events from the repository-root `eve.json` file.
- **SOC dashboard:** summary counters, recent alert queue, severity filter and text search.
- **SQLite storage:** creates the schema automatically in ignored local runtime storage; supports stable event fingerprints to prevent repeat imports.
- **Test automation:** unit tests run through GitHub Actions on pushes and pull requests.

## Project layout

```text
cyber-range-ids-soc-dashboard/
├── dashboard/
│   ├── app.py
│   └── templates/
│       └── index.html
├── database/
│   ├── __init__.py
│   └── db.py
├── detection/
│   └── engine.py
├── ids/
│   └── ids_parser.py
├── red_team/
│   ├── safety.py
│   ├── port_scanner.py
│   ├── brute_force.py
│   ├── web_attack.py
│   ├── ddos_simulator.py
│   └── dos_simulator.py
├── response/
│   └── ips.py
├── tests/
│   └── test_core.py
├── .github/workflows/tests.yml
├── eve.json
├── requirements.txt
└── README.md
```

## Run locally

Python 3.10+ is recommended.

### 1. Create and activate a virtual environment

Linux / Kali / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the dashboard

Run this from the repository root:

```bash
python dashboard/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

The app binds to loopback by default. It does not enable Flask debug mode. The local SQLite database is created at `instance/cyber_range.sqlite3`; that runtime directory is excluded from Git.

Optional environment variables:

- `CYBER_RANGE_DB_PATH`: use a different SQLite file path.
- `CYBER_RANGE_SECRET_KEY`: set a stable Flask session secret for a persistent local deployment.
- `PORT`: choose a different local HTTP port.

## Using the dashboard

1. Keep the target as `127.0.0.1` for a first run, or use a private lab IPv4 address such as `192.168.56.10` that you control.
2. Select one of the scenarios and run it.
3. Review the generated alert in the queue.
4. Use the severity selector or search field to narrow the results.
5. To import IDS data, put Suricata EVE JSON alert records in the configured root-level `eve.json` file and select **Import Suricata EVE alerts**.

The importer skips malformed JSON lines and non-alert events. It fingerprints source lines so importing the same events again does not create duplicates.

## Test

Run the unit tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the same command on pushes and pull requests.

## Safety and limitations

- Target checks accept private or loopback IPv4 addresses only; public IPs, domain names, IPv6, multicast, link-local and unspecified addresses are rejected.
- The port check connects only to TCP ports 21, 22, 23, 80 and 443, with a short timeout.
- Brute-force, web and DDoS scenarios print representative events only. They do not attempt credentials, send HTTP exploit requests or transmit a traffic flood.
- `response/ips.py` maintains an in-memory demonstration set. It does not block traffic at the operating-system level, and its state is lost when the process exits.
- EVE import is manual, not a live tail or streaming pipeline. The included `eve.json` is only a sample event, not proof that Suricata is running.
- Classification is basic signature matching. An alert is an investigation lead, not proof that an attack succeeded.
- Authentication, multi-user roles, real firewall integration, a live Suricata service and automated response approvals are not implemented.

## Planned next steps

1. Add structured incident triage: New, Investigating, False Positive and Closed.
2. Add rule tuning and repeatable detection test cases.
3. Add live Suricata event ingestion with checkpointing and operational health checks.
4. Add an isolated lab topology and Purple Team detection coverage reports.
5. Integrate Hermes Agent as an analyst assistant for alert summaries and investigation suggestions. Keep model output advisory; never let it execute response actions without explicit human approval.
6. Revisit Windows/Active Directory telemetry as a separate lab integration (Windows Security events or a small AD simulation), after the core SOC workflow is stable.

## References

- [Flask documentation](https://flask.palletsprojects.com/)
- [Suricata documentation](https://docs.suricata.io/)
- [Python documentation](https://docs.python.org/3/)
- [SQLite documentation](https://www.sqlite.org/docs.html)

## Author

**Dileep P. O.**  
Computer Science and Engineering · Cybersecurity | Network Security | Security Operations

## Disclaimer

This project is for educational and authorised cybersecurity testing only. Do not use it against systems or networks without permission.
