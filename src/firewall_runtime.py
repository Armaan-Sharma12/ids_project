import sys
import os
import time
import socket
import collections
import numpy as np
import joblib
from scapy.all import sniff, IP, TCP, UDP, conf
from keras.models import load_model
from mitigation_engine import get_mitigation_decision, execute_response
from Dashboard.db import log_event


# ==============================
# CONFIGURATION
# ==============================
PacketBuffer = collections.deque(maxlen=20) 
BLOCKED_IPS = set()

# Paths
MODEL_PATH = r"models\attack_classifier\ids_cnn_lstm.h5"
SCALER_PATH = r"models\attack_classifier\scaler_2018.save"
ENCODER_PATH = r"models\attack_classifier\encoder_2018.save"

# ⚠️ EXACT 16 FEATURES (Must match your Training Script)
TARGET_FEATURES = [
    'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max', 
    'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 
    'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow IAT Mean', 
    'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min'
]

# ==============================
# FLOW TRACKER
# ==============================
class FlowTracker:
    def __init__(self):
        self.flows = {} # {ip: {start_time, last_seen, count, iat_list}}

    def get_stats(self, src_ip):
        now = time.time()
        if src_ip not in self.flows:
            self.flows[src_ip] = {'start': now, 'last': now, 'count': 1, 'iat': []}
            return 1, 0, 1 
        
        f = self.flows[src_ip]
        duration_sec = now - f['start']
        iat_sec = now - f['last']
        
        f['last'] = now
        f['count'] += 1
        f['iat'].append(iat_sec)
        
        iat_mean_sec = np.mean(f['iat']) if f['iat'] else 0
        
        # Reset if idle > 60s
        if iat_sec > 60:
             self.flows[src_ip] = {'start': now, 'last': now, 'count': 1, 'iat': []}
             return 1, 0, 1
             
        # Return Microseconds (1s = 1,000,000us)
        return (duration_sec * 1_000_000), (iat_mean_sec * 1_000_000), f['count']

tracker = FlowTracker()

# ==============================
# FEATURE EXTRACTOR (Fixed to 16 Features)
# ==============================
def extract_features(packet):
    try:
        if IP not in packet: return None
        src_ip = packet[IP].src
        
        # Get Stats (Microseconds)
        dur_us, iat_mean_us, count = tracker.get_stats(src_ip)
        
        feat = {}
        pkt_len = len(packet)
        
        if TCP in packet: feat['Destination Port'] = packet[TCP].dport
        elif UDP in packet: feat['Destination Port'] = packet[UDP].dport
        else: feat['Destination Port'] = 0
            
        feat['Flow Duration'] = dur_us
        feat['Total Fwd Packets'] = count
        feat['Total Backward Packets'] = 0
        feat['Total Length of Fwd Packets'] = pkt_len * count
        feat['Total Length of Bwd Packets'] = 0
        
        feat['Fwd Packet Length Max'] = pkt_len
        feat['Fwd Packet Length Min'] = pkt_len
        feat['Fwd Packet Length Mean'] = pkt_len
        feat['Bwd Packet Length Max'] = 0
        feat['Bwd Packet Length Min'] = 0
        feat['Bwd Packet Length Mean'] = 0
        
        # Removed 'Flow Bytes/s' and 'Flow Packets/s' to match model
        
        feat['Flow IAT Mean'] = iat_mean_us
        feat['Flow IAT Std'] = 0 
        feat['Flow IAT Max'] = iat_mean_us
        feat['Flow IAT Min'] = iat_mean_us
        
        return [feat[col] for col in TARGET_FEATURES]
    except:
        return None

# ==============================
# MAIN PROCESSOR
# ==============================
def process_packet(packet):
    global model, scaler, encoder
    if IP not in packet: return
    src_ip = packet[IP].src
    
    if src_ip in BLOCKED_IPS: return

    features = extract_features(packet)
    if features is None: return

    # Check for mismatch before crashing
    if len(features) != 16:
        print(f"❌ ERROR: Extracted {len(features)} features, expected 16.")
        return

    PacketBuffer.append(features)

    if len(PacketBuffer) >= 1: 
        latest_feat = np.array(features).reshape(1, -1)
        
        try:
            scaled = scaler.transform(latest_feat)
            input_data = scaled.reshape(1, 16, 1) # Matches (1, 16, 1) shape
            
            pred = model.predict(input_data, verbose=0)
            conf = np.max(pred)
            label = encoder.classes_[np.argmax(pred)]
            
            decision = get_mitigation_decision(src_ip, label, conf)
            action = decision['action']
            
            # --- DEBUG OUTPUT ---
            status = f"[{action}] {src_ip} -> {label} ({conf*100:.1f}%)"
            
            if action == 'BLOCK':
                print(f"\n🚨 {status} | 🚫 BLOCKING!")
                execute_response(src_ip, decision)
                BLOCKED_IPS.add(src_ip)
            elif action == 'MONITOR':
                if label == 'Benign':
                    # Overwrite line for clean view
                    print(f"\r[.] {status}      ", end="") 
                else:
                    print(f"\n⚠️ {status} | Reason: {decision['reason']}")
            elif action == 'ALLOW':
                 print(f"\r[√] {status}      ", end="")
            log_event(src_ip, label, conf, action, decision['reason'])
            

        except Exception as e:
            print(f"\n❌ Prediction Error: {e}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"

# ==============================
# STARTUP
# ==============================
if __name__ == "__main__":
    print("[INIT] Loading CNN-LSTM Model...")
    try:
        model = load_model(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoder = joblib.load(ENCODER_PATH)
        print("✅ Brain Loaded.")
    except Exception as e:
        print(f"❌ Model Error: {e}")
        sys.exit(1)

    my_ip = get_local_ip()
    print(f"[*] My IP: {my_ip}")
    
    # Auto-detect best interface
    try:
        # Windows often calls Wi-Fi just "Wi-Fi"
        # If this fails, it falls back to default
        iface = "Wi-Fi"
        print(f"[*] Attempting to listen on: {iface}")
        sniff(iface=iface, prn=process_packet, store=0)
    except Exception:
        print(f"⚠️ 'Wi-Fi' interface not found. Trying default...")
        sniff(prn=process_packet, store=0)