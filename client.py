import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        receive_thread.start()

    def send(self, message):
        try:
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print("Error sending message:", e)

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message)
                else:
                    break
            except Exception as e:
                print("Error receiving message:", e)
                break

if __name__ == "__main__":
    SERVER_HOST = 'localhost'
    SERVER_PORT = 12345
    client = ChatClient(SERVER_HOST, SERVER_PORT)
    print("Connected to server. Start typing messages:")
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client.send(message)
    client.client_socket.close()
