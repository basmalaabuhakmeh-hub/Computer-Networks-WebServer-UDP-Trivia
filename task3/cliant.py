import socket
import threading
import sys

class TriviaClient:
    def __init__(self, server_ip, server_port, username):
        self.server_address = (server_ip, server_port)
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.sock.sendto(self.username.encode('utf-8'), self.server_address)
        threading.Thread(target=self.listen_to_server, daemon=True).start()

        while True:
            try:
                message = input("")
                if message.lower() == "quit":
                    print("Exiting game...")
                    self.sock.sendto("quit".encode('utf-8'), self.server_address)
                    sys.exit(0)
                self.sock.sendto(message.encode('utf-8'), self.server_address)
            except SystemExit:
                break

    def listen_to_server(self):
        while True:
            try:
                response, _ = self.sock.recvfrom(1024)
                print(response.decode('utf-8'))
            except:
                break


if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    username = input("Enter your username: ")

    client = TriviaClient(server_ip, server_port, username)
    client.start()