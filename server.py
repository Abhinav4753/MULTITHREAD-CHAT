import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(5)
        print("Server started on {}:{}".format(self.host, self.port))
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Client {} connected".format(client_address))
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.daemon = True
            client_handler.start()

    def handle_client(self, client_socket, client_address):
        self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print("Received message from {}: {}".format(client_address, message))
                    self.broadcast(message, client_socket)
                else:
                    self.remove_client(client_socket, client_address)
                    break
            except Exception as e:
                print("Error:", e)
                self.remove_client(client_socket, client_address)
                break

    def broadcast(self, message, sender_socket):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                except Exception as e:
                    print("Error broadcasting to client:", e)
                    self.remove_client(client_socket, client_socket.getpeername())

    def remove_client(self, client_socket, client_address):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()
            print("Client {} disconnected".format(client_address))

if __name__ == "__main__":
    SERVER_HOST = 'localhost'
    SERVER_PORT = 12345
    server = ChatServer(SERVER_HOST, SERVER_PORT)
    server.start()
