import socket
import threading
import os

class P2PPeer:
    def __init__(self, host='0.0.0.0', port=12345, peer_ip=None, peer_port=None):
        self.host = host
        self.port = port
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Peer listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            filename = client_socket.recv(1024).decode().strip()
            if not filename:
                return
            print(f"Request received for file: {filename}")
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    data = f.read()
                client_socket.sendall(len(data).to_bytes(4, 'big'))  # Send size
                client_socket.sendall(data)
                print(f"File '{filename}' sent.")
            else:
                client_socket.sendall((0).to_bytes(4, 'big'))  # Size 0 for not found
                print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def start_server(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def send_file(self, filename):
        if not self.peer_ip or not self.peer_port:
            print("No peer specified.")
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.peer_ip, self.peer_port))
            sock.sendall(filename.encode())
            size_bytes = sock.recv(4)
            size = int.from_bytes(size_bytes, 'big')
            if size == 0:
                print("File not found on peer.")
                return
            data = b''
            while len(data) < size:
                packet = sock.recv(4096)
                if not packet:
                    break
                data += packet
            received_filename = f"received_{filename}"
            with open(received_filename, 'wb') as f:
                f.write(data)
            print(f"File received and saved as '{received_filename}' (size: {size} bytes).")
        except Exception as e:
            print(f"Error sending/receiving file: {e}")
        finally:
            sock.close()