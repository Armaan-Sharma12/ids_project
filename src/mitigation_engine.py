import time
import threading
import subprocess
from collections import defaultdict

# ==============================
# 1. STATE TRACKER (Memory)
# ==============================
class StateTracker:
    def __init__(self, decay_interval=60):
        self._history = defaultdict(lambda: {
            'counts': defaultdict(int), 
            'last_seen': 0
        })
        self._lock = threading.Lock()
        self._decay_interval = decay_interval 

    def update_and_get_count(self, src_id, label):
        current_time = time.time()
        with self._lock:
            entry = self._history[src_id]
            last_seen = entry['last_seen']
            
            # Decay logic (Leaky Bucket)
            if last_seen > 0:
                elapsed = current_time - last_seen
                decay_amount = int(elapsed // self._decay_interval)
                if decay_amount > 0:
                    for k in entry['counts']:
                        entry['counts'][k] = max(0, entry['counts'][k] - decay_amount)

            entry['counts'][label] += 1
            entry['last_seen'] = current_time
            return entry['counts'][label]

tracker = StateTracker(decay_interval=30)
BLOCKED_IPS = set()

# ==============================
# 2. CONFIGURATION & MAPPING
# ==============================
# Map specific 2018 labels to Broad Categories
ATTACK_MAPPING = {
    'Benign': 'BENIGN',
    
    # DDoS Variants (High Volume)
    'DDOS attack-LOIC-UDP': 'DDoS',
    'DDOS attack-HOIC': 'DDoS',
    'DDoS attacks-LOIC-HTTP': 'DDoS',
    
    # DoS Variants (Low Volume, Slow)
    'DoS attacks-GoldenEye': 'DoS',
    'DoS attacks-Slowloris': 'DoS',
    
    # Botnet (Command & Control)
    'Bot': 'Botnet',
    
    # Brute Force = PortScan behavior
    'FTP-BruteForce': 'PortScan',
    'SSH-Bruteforce': 'PortScan'
}

CONF_THRESHOLDS = {
    'DDoS': 0.60,      
    'Botnet': 0.70,    
    'PortScan': 0.60,  
    'DoS': 0.60
}

# How many times we see it before blocking
ESCALATION_LIMITS = {
    'DDoS': 2,        # Block fast
    'Botnet': 3,
    'PortScan': 5,    # Allow a few accidental packets
    'DoS': 3
}

WHITELIST_IPS = [
    "127.0.0.1", "0.0.0.0", "8.8.8.8",
    "192.168.1.1" # Gateway only - DO NOT whitelist your PC if testing!
]

# ==============================
# 3. MITIGATION LOGIC
# ==============================
def is_whitelisted(ip):
    if ip in WHITELIST_IPS: return True
    if ip.startswith("20.") or ip.startswith("52."): return True # Microsoft/Azure
    return False

def get_mitigation_decision(src_id, raw_label, confidence):
    """
    1. Maps specific label to Category (e.g., 'DDOS-HOIC' -> 'DDoS')
    2. Checks Thresholds & Whitelists
    3. Returns Decision
    """
    if is_whitelisted(src_id):
        return {'action': 'ALLOW', 'severity': 'NONE', 'reason': 'Whitelisted'}
    
    # 1. Normalize Label (The Translation Step)
    category = ATTACK_MAPPING.get(raw_label, 'UNKNOWN')
    
    if category == 'BENIGN':
        return {'action': 'ALLOW', 'severity': 'NONE', 'reason': 'Benign'}

    # 2. Update State
    hits = tracker.update_and_get_count(src_id, category)

    # 3. Check Confidence
    required_conf = CONF_THRESHOLDS.get(category, 0.65)
    if confidence < required_conf:
        return {'action': 'MONITOR', 'severity': 'LOW', 'reason': f'Low Conf ({confidence:.2f})'}

    # 4. Escalation Rules
    limit = ESCALATION_LIMITS.get(category, 5)
    
    if hits >= limit:
        return {'action': 'BLOCK', 'severity': 'CRITICAL', 'reason': f'Confirmed {category} ({raw_label})'}
    
    return {'action': 'MONITOR', 'severity': 'MEDIUM', 'reason': f'Suspected {category} ({hits}/{limit})'}

# ==============================
# 4. EXECUTION
# ==============================
def execute_response(src_ip, decision):
    action = decision['action']
    reason = decision['reason']
    
    if action == 'BLOCK':
        if src_ip in BLOCKED_IPS:
            return 
            
        print(f"🚫 BLOCKING {src_ip} | Reason: {reason}")
        try:
            rule_name = f"AI_Block_{src_ip}"
            # Windows Firewall Block Command
            subprocess.run(
                f"netsh advfirewall firewall add rule name=\"{rule_name}\" dir=in action=block remoteip={src_ip}",
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            BLOCKED_IPS.add(src_ip)
            print(f"✅ {src_ip} Successfully Isolated.")
        except Exception as e:
            print(f"❌ Block Failed: {e}")