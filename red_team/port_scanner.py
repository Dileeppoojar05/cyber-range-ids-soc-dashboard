import socket
import sys

def scan(target):
    print(f"[SCAN] Target: {target}")

    ports = [21, 22, 23, 80, 443]

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
        else:
            print(f"[CLOSED] Port {port}")

        sock.close()

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else input("Enter target IP: ")
    scan(target)
