import socket
import threading
import time
import random

# 🎯 CONFIGURATION
TARGET_IP = "192.168.1.1" 
START_PORT = 1
END_PORT = 1000

def scan_worker(ports):
    for port in ports:
        try:
            # Create standard socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            
            # Connect (Scan)
            result = s.connect_ex((TARGET_IP, port))
            s.close()
            
            # 🎯 CRITICAL: Add delay to match "PortScan" signature
            # Your training data showed PortScan IAT is higher (~70ms) compared to DoS (~10ms)
            # We sleep for 0.05s to 0.1s to mimic this behavior.
            time.sleep(random.uniform(0.01, 0.05))

        except:
            pass

def run_portscan():
    print(f"\n[🔎] Launching PORTSCAN SIMULATION against {TARGET_IP}...")
    print("    Pattern: Connection attempts to range 1-1000")
    print("    Goal:    Trigger 'PortScan' detection (Slower IAT)")

    # Split ports among threads for efficiency, but keep it controlled
    ports = list(range(START_PORT, END_PORT))
    random.shuffle(ports) # Randomize order
    
    # Use fewer threads to prevent it from looking like a DoS flood
    thread_count = 10 
    chunk_size = len(ports) // thread_count
    
    threads = []
    
    for i in range(thread_count):
        chunk = ports[i*chunk_size : (i+1)*chunk_size]
        t = threading.Thread(target=scan_worker, args=(chunk,))
        threads.append(t)
        t.start()
        
    print(f"    🚀 Scanning with {thread_count} threads...")
    
    for t in threads:
        t.join()
        
    print("\n[✅] Scan Complete.")

if __name__ == "__main__":
    run_portscan()