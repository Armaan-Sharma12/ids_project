import socket
import time
import sys
import random

# 🎯 CONFIGURATION
TARGET_IP = "192.168.1.1"  # Router
START_PORT = 20
END_PORT = 100

def stealth_scan():
    print(f"\n[🕵️] Launching STEALTH SCAN against {TARGET_IP}...")
    print("    Pattern: Single Thread, Variable Delay")
    print("    Goal:    Match 'PortScan' profile (High IAT)")

    for port in range(START_PORT, END_PORT):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            
            # The Scan
            result = s.connect_ex((TARGET_IP, port))
            if result == 0:
                print(f"    found open port: {port}")
            
            s.close()

            # 🎯 CRITICAL: The "Human" Delay
            # DoS IAT is ~10ms. We want ~100ms - 500ms for PortScan.
            delay = random.uniform(0.1, 0.3) 
            time.sleep(delay)

            if port % 10 == 0:
                print(f"    Scanned port {port} (Delay: {delay*1000:.0f}ms)...")

        except KeyboardInterrupt:
            print("\n[🛑] Scan Stopped.")
            sys.exit()
        except:
            pass

if __name__ == "__main__":
    stealth_scan()