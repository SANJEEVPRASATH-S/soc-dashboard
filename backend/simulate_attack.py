import requests
import time

API = "http://localhost:8000/api/alerts"

print("Simulating Brute Force Attack...")

for i in range(5):
    response = requests.post(API, params={
        "severity": "critical",
        "message": f"Brute force attempt #{i+1} — ssh.prod-server from 192.168.1.100",
        "status": "new",
        "ip": "192.168.1.100"
    })
    print(f"Alert {i+1} sent!")
    time.sleep(2)

print("Done! Check your dashboard!")
