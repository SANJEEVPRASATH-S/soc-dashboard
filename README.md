# 🛡️ SOC Command Center Dashboard

A real-time Security Operations Center (SOC) dashboard for monitoring network threats, security alerts, and incident response — built with FastAPI, SQLite, and vanilla JavaScript.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Overview

This project simulates a real-world Security Operations Center dashboard used by cybersecurity analysts to monitor active threats, track incidents, and respond to security alerts in real time. It demonstrates how raw security event data can be ingested, stored, and visualized for rapid decision-making.

---

## ✨ Features

- **Live Metrics** — Active threats, open incidents, MTTR (Mean Time to Resolve), and system health, auto-refreshing every 10 seconds
- **Real-Time Alert Feed** — Severity-coded alerts (Critical / High / Medium / Low) with status tracking (New / Active / Closed)
- **Search & Filter** — Filter alerts by severity, status, or search by IP address / message
- **Browser Notifications** — Instant toast and native browser notifications when a new critical/high alert is created
- **Persistent Database** — SQLite backend stores alerts and incidents permanently (survives refresh/restart)
- **Threat Intelligence Panels** — Threat category breakdown, top source IPs, system health table, and incident timeline
- **REST API** — Fully documented OpenAPI/Swagger interface for integration with external tools
- **Attack Simulator** — Python script to simulate live brute-force attacks for demo/testing purposes

---

## 🏗️ Tech Stack

| Layer       | Technology              |
|-------------|--------------------------|
| Backend     | Python, FastAPI          |
| Database    | SQLite, SQLAlchemy ORM   |
| Frontend    | HTML, CSS, JavaScript    |
| API Docs    | Swagger UI (auto-generated) |

---

## 📁 Project Structure

```
soc-dashboard/
├── backend/
│   ├── main.py              # FastAPI application & API routes
│   ├── simulate_attack.py   # Script to simulate live brute-force alerts
│   ├── requirements.txt     # Python dependencies
│   └── soc.db               # SQLite database (auto-created on first run)
├── frontend/
│   └── index.html           # Dashboard UI (also served by backend at "/")
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/soc-dashboard.git
cd soc-dashboard/backend

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn main:app --reload --port 8000
```

Open your browser at:
```
http://localhost:8000
```

The dashboard, API, and database all run from this single command — no separate frontend server needed.

### API Documentation

Interactive Swagger docs available at:
```
http://localhost:8000/docs
```

---

## 🎯 Demo: Simulate a Live Attack

To see the dashboard update in real time, run the included attack simulator in a separate terminal:

```bash
cd backend
python simulate_attack.py
```

This sends 5 simulated brute-force alerts to the API every 2 seconds — watch them appear instantly on the dashboard.

---

## 📡 API Endpoints

| Method | Endpoint                | Description                          |
|--------|--------------------------|---------------------------------------|
| GET    | `/api/all`               | Full dashboard data in one call       |
| GET    | `/api/metrics`            | Active threats, incidents, MTTR       |
| GET    | `/api/alerts`              | All stored alerts                     |
| POST   | `/api/alerts`              | Create a new alert                    |
| PUT    | `/api/alerts/{alert_id}`  | Update an alert's status              |
| GET    | `/api/incidents`           | Incident timeline                     |
| GET    | `/api/systems`             | System health status                  |
| GET    | `/api/source-ips`          | Top attacker IPs                      |
| GET    | `/api/threat-categories`   | Threat type breakdown                 |
| GET    | `/api/alert-volume`        | 12-hour alert volume histogram        |

---

## 🔌 Connecting Real Data Sources

This project ships with mock data for demonstration. To connect a real SIEM:

**Splunk:**
```python
import splunklib.client as client
service = client.connect(host='splunk-host', port=8089, username='admin', password='...')
```

**Elasticsearch:**
```python
from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200')
```

Map the response from your SIEM to the same JSON shape used in `main.py`'s mock data, and the dashboard will work unchanged.



## 📌 Roadmap / Future Enhancements

- WhatsApp / SMS alerting for critical incidents (Twilio integration)
- World map visualization of attacker geolocation
- MITRE ATT&CK technique mapping
- Login-based brute-force detection module
- PDF/Excel report export

---



