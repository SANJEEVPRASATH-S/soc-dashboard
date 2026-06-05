from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import random

# ---- Database Setup ----
SQLALCHEMY_DATABASE_URL = "sqlite:///./soc.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AlertModel(Base):
    __tablename__ = "alerts"
    id         = Column(Integer, primary_key=True, index=True)
    severity   = Column(String)
    message    = Column(String)
    status     = Column(String)
    ip         = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class IncidentModel(Base):
    __tablename__ = "incidents"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String)
    priority   = Column(String)
    color      = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- App ----
app = FastAPI(title="SOC Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Serve Frontend ----
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse("index.html")

# ---- Mock Data ----
ALERTS = [
    {"id": "ALT-001", "severity": "critical", "message": "Brute force attempt — ssh.prod-us-east-01",   "status": "new",    "time": "00:42", "ip": "185.220.101.47"},
    {"id": "ALT-002", "severity": "critical", "message": "C2 beacon detected — 185.220.101.47",          "status": "active", "time": "00:38", "ip": "45.155.204.12"},
    {"id": "ALT-003", "severity": "high",     "message": "Privilege escalation — svc_deploy@db-cluster", "status": "active", "time": "00:31", "ip": "194.165.16.29"},
    {"id": "ALT-004", "severity": "high",     "message": "Exfil: 4.2 GB outbound to 45.155.204.12",      "status": "new",    "time": "00:27", "ip": "45.155.204.12"},
    {"id": "ALT-005", "severity": "medium",   "message": "Lateral movement — workstation WS-0047",        "status": "active", "time": "00:19", "ip": "103.214.163.5"},
    {"id": "ALT-006", "severity": "medium",   "message": "Anomalous DNS queries — hr-laptop-12",          "status": "closed", "time": "00:11", "ip": "23.94.171.40"},
    {"id": "ALT-007", "severity": "low",      "message": "Failed MFA attempts (8x) — admin@corp.io",     "status": "closed", "time": "00:04", "ip": "91.108.4.212"},
]

INCIDENTS = [
    {"id": "INC-2041", "title": "Brute force escalated to P1",            "priority": "P1", "time": "00:42", "color": "#E24B4A"},
    {"id": "INC-2040", "title": "Analyst blocked exfil host",             "priority": "P2", "time": "00:35", "color": "#EF9F27"},
    {"id": "INC-2039", "title": "Playbook PB-17 triggered automatically", "priority": "P2", "time": "00:28", "color": "#378ADD"},
    {"id": "INC-2038", "title": "Assigned to Tier 2 analyst",             "priority": "P3", "time": "00:19", "color": "#EF9F27"},
    {"id": "INC-2037", "title": "Closed — False positive confirmed",      "priority": "P4", "time": "00:07", "color": "#1D9E75"},
]

SYSTEMS = [
    {"name": "SIEM Core",        "status": "healthy",  "uptime": 99.9},
    {"name": "Firewall cluster", "status": "healthy",  "uptime": 99.7},
    {"name": "EDR agents",       "status": "degraded", "uptime": 96.2},
    {"name": "VPN gateway",      "status": "healthy",  "uptime": 100.0},
    {"name": "Log ingestion",    "status": "critical", "uptime": 81.4},
    {"name": "Threat intel API", "status": "healthy",  "uptime": 98.8},
]

SOURCE_IPS = [
    {"ip": "185.220.101.47", "country": "RU", "hits": 841, "level": "critical"},
    {"ip": "45.155.204.12",  "country": "CN", "hits": 703, "level": "critical"},
    {"ip": "194.165.16.29",  "country": "IR", "hits": 412, "level": "warning"},
    {"ip": "91.108.4.212",   "country": "KP", "hits": 299, "level": "warning"},
    {"ip": "103.214.163.5",  "country": "BR", "hits": 187, "level": "info"},
    {"ip": "23.94.171.40",   "country": "US", "hits": 94,  "level": "normal"},
]

CATEGORIES = [
    {"name": "Malware",        "percent": 34, "color": "#E24B4A"},
    {"name": "Phishing",       "percent": 27, "color": "#EF9F27"},
    {"name": "Insider threat", "percent": 18, "color": "#378ADD"},
    {"name": "Ransomware",     "percent": 13, "color": "#7F77DD"},
    {"name": "Recon / scan",   "percent": 8,  "color": "#888780"},
]

ALERT_VOLUME = {
    "labels": ["12h","11h","10h","9h","8h","7h","6h","5h","4h","3h","2h","1h"],
    "data":   [4, 7, 5, 9, 12, 8, 14, 11, 17, 22, 18, 14]
}

# Live counters
_state = {"threats": 14, "incidents": 27}

def fluctuate():
    if random.random() < 0.3:
        _state["threats"]   = max(0, _state["threats"]   + random.choice([-1, 1]))
    if random.random() < 0.15:
        _state["incidents"] = max(0, _state["incidents"] + random.choice([-1, 1]))

# ---- Startup: create tables + seed DB ----
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(AlertModel).count() == 0:
        for a in ALERTS:
            db.add(AlertModel(severity=a["severity"], message=a["message"], status=a["status"], ip=a["ip"]))
        db.commit()
    if db.query(IncidentModel).count() == 0:
        for i in INCIDENTS:
            db.add(IncidentModel(title=i["title"], priority=i["priority"], color=i["color"]))
        db.commit()
    db.close()

# ---- Routes ----
@app.get("/api/metrics")
def get_metrics():
    fluctuate()
    return {
        "active_threats":  _state["threats"],
        "open_incidents":  _state["incidents"],
        "mttr_minutes":    38,
        "healthy_systems": 94,
        "total_systems":   151,
        "healthy_count":   142,
        "timestamp":       datetime.now(timezone.utc).isoformat(),
    }

@app.get("/api/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(AlertModel).order_by(AlertModel.created_at.desc()).all()
    return {"alerts": [
        {
            "id":       a.id,
            "severity": a.severity,
            "message":  a.message,
            "status":   a.status,
            "ip":       a.ip,
            "time":     a.created_at.strftime("%H:%M")
        } for a in alerts
    ]}

@app.post("/api/alerts")
def create_alert(severity: str, message: str, status: str = "new", ip: str = "", db: Session = Depends(get_db)):
    alert = AlertModel(severity=severity, message=message, status=status, ip=ip)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"success": True, "id": alert.id}

@app.put("/api/alerts/{alert_id}")
def update_alert(alert_id: int, status: str, db: Session = Depends(get_db)):
    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if alert:
        alert.status = status
        db.commit()
    return {"success": True}

@app.get("/api/incidents")
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(IncidentModel).order_by(IncidentModel.created_at.desc()).all()
    return {"incidents": [
        {
            "id":       f"INC-{i.id+2036}",
            "title":    i.title,
            "priority": i.priority,
            "color":    i.color,
            "time":     i.created_at.strftime("%H:%M")
        } for i in incidents
    ]}

@app.get("/api/systems")
def get_systems():
    return {"systems": SYSTEMS}

@app.get("/api/source-ips")
def get_source_ips():
    return {"source_ips": SOURCE_IPS}

@app.get("/api/threat-categories")
def get_threat_categories():
    return {"categories": CATEGORIES}

@app.get("/api/alert-volume")
def get_alert_volume():
    return ALERT_VOLUME

@app.get("/api/all")
def get_all(db: Session = Depends(get_db)):
    fluctuate()
    alerts = db.query(AlertModel).order_by(AlertModel.created_at.desc()).all()
    incidents = db.query(IncidentModel).order_by(IncidentModel.created_at.desc()).all()
    return {
        "metrics": {
            "active_threats":  _state["threats"],
            "open_incidents":  _state["incidents"],
            "mttr_minutes":    38,
            "healthy_systems": 94,
            "total_systems":   151,
            "healthy_count":   142,
        },
        "alerts": [
            {"id": a.id, "severity": a.severity, "message": a.message,
             "status": a.status, "ip": a.ip, "time": a.created_at.strftime("%H:%M")}
            for a in alerts
        ],
        "incidents": [
            {"id": f"INC-{i.id+2036}", "title": i.title, "priority": i.priority,
             "color": i.color, "time": i.created_at.strftime("%H:%M")}
            for i in incidents
        ],
        "systems":      SYSTEMS,
        "source_ips":   SOURCE_IPS,
        "categories":   CATEGORIES,
        "alert_volume": ALERT_VOLUME,
        "timestamp":    datetime.now(timezone.utc).isoformat(),
    }