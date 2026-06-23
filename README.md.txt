# 🛡️ Cyber Range IDS & SOC Dashboard

## 📌 Overview

Cyber Range IDS & SOC Dashboard is a cybersecurity project designed to simulate a real-world Security Operations Center (SOC). It demonstrates how cyber attacks are generated, detected, and monitored through a centralized dashboard.

This project helps in understanding:

* 🔴 Red Team (Attack Simulation)
* 🔵 Blue Team (Detection & Monitoring)
* 🟣 Purple Team (Combined Analysis)

---

## 🎯 Features

* Simulated cyber attacks (DDoS, Port Scan, SQL Injection)
* Intrusion Detection System (IDS) log monitoring
* Real-time SOC dashboard using Flask
* Alert generation and visualization
* Threat activity tracking

---

## 📁 Project Structure

```text
cyber-range/
├── main.py
├── eve.json
├── dashboard/
│   └── app.py
├── red_team/
│   └── simulator.py
├── ids/
│   └── ids_parser.py
└── requirements.txt
```

---

## ⚙️ Requirements

* Python 3.x
* pip (Python package manager)

---

## 📦 Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### 1️⃣ Start the SOC Dashboard

```bash
cd dashboard
python3 app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

### 2️⃣ Run Attack Simulator (Red Team)

```bash
cd red_team
python3 simulator.py
```

---

### 3️⃣ Run IDS Parser (Blue Team)

```bash
cd ids
python3 ids_parser.py
```

---

## 🔄 Workflow

1. Red Team generates simulated attacks
2. Logs are stored in `eve.json`
3. IDS parser analyzes logs
4. Dashboard displays alerts and threat activity

---

## ⚠️ Limitations

* Uses simulated attack data
* No real IDS integration (e.g., Suricata/Snort)
* No database (temporary data only)

---

## 💡 Future Improvements

* Integrate real IDS tools (Suricata, Snort)
* Add database support (MongoDB / MySQL)
* Enhance UI/UX (dark hacker-style dashboard)
* Add authentication system
* Real-time WebSocket updates

---

## 🎓 Use Case

* Cybersecurity learning & practice
* SOC simulation environment
* Internship and portfolio project

---

## 👨‍💻 Author

Developed as a cybersecurity learning project for practical SOC and IDS understanding.
