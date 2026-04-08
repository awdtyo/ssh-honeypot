import socket
import threading
import paramiko
import logging
import argparse

logging.basicConfig(
    filename="logs/honeypot.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

HOST_KEY = paramiko.RSAKey(filename="honeypot_rsa")

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        logging.info(f"LOGIN ATTEMPT | IP: {self.client_ip} | user: {username} | pass: {password}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

def handle_connection(client_socket, client_addr):
    ip = client_addr[0]
    logging.info(f"CONNECTION | IP: {ip}")
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(HOST_KEY)
        server = FakeSSHServer(ip)
        transport.start_server(server=server)
        transport.join(timeout=10)
    except Exception as e:
        logging.error(f"ERROR | IP: {ip} | {e}")
    finally:
        client_socket.close()

def start_honeypot(port=2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(100)
    print(f"[+] Honeypot listening on port {port}...")
    while True:
        client, addr = sock.accept()
        t = threading.Thread(target=handle_connection, args=(client, addr))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH Honeypot")
    parser.add_argument("--port", type=int, default=2222, help="Port to listen on")
    args = parser.parse_args()
    start_honeypot(port=args.port)