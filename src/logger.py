import json
import os
from datetime import datetime

LOG_FILE = "logs/firewall_logs.json"

os.makedirs("logs", exist_ok=True)

def log_event(src_ip, label, confidence, action, reason):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "src_ip": src_ip,
        "label": label,
        "confidence": float(confidence),
        "action": action,
        "reason": reason
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(log_entry)

        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Logging error:", e)
