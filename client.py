import socket
from enum import Enum
# This program accepts ip, port, name of encoded file, and name of decoded file as arguments

class ClientState(Enum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    SENDING = 3
    RECEIVING = 4
    DISCONNECTED = 5


class ClientSocket:
    def __init__(self, host_ip: str, host_port:str, file:str, key:str):
        self.host_ip = host_ip
        self.host_port = host_port
        self.message = read_file(file)
        self.key = key
        self.state = ClientState.INIT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def validate_inputs(self):
        pass

    def read_file(self, file):
        try:
            with open(file) as f:
                self.message = f.read()
        except Exception as e:
            print("File Error", e)

    def format_payload(self):
        return self.message + '&' + self.key


    def connect(self):
        self.state = ClientState.CONNECTING
        try:
            self.client_socket.connect((self.host_ip, self.host_port))
            self.state = ClientState.CONNECTED
            print("Socket Successfully Created")
        except Exception as e:
            print("Connection Failed:", e)
            self.state=ClientState.DISCONNECTED

    def send_data(self):
        if self.state == ClientState.CONNECTED:
            payload = self.format_payload()
            try:
                self.client_socket.send(payload.encode())
                self.state = ClientState.SENDING
                self.listening()
            except Exception as e:
                print("Sending Error:", e)

    def listening(self):
        if self.state == ClientState.SENDING:
            self.state = ClientState.RECEIVING
            response = self.client_socket.recv(1024).decode()
            print("Recieved: ", response)
            self.client_socket.close()
            self.state = ClientState.DISCONNECTED
        else:
            print("Error in Sending/Receiving")
            self.client_socket.close()
            self.state = ClientState.DISCONNECTED



def arg_parser():
    pass


def read_file(file) -> str:
    with open(file, 'r') as f:
        return f.read()


def main():
    host = '127.0.0.1'
    port = 3333
    print("Client listening on Address", host, " and port: ", port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    message = read_file("test.txt")
    key = 'aaabbb'
    message = message + '&' + key
    # Sending
    server_socket.send(message.encode())

    # Received
    data = server_socket.recv(1024).decode()
    print("Received from server: ", data)

    server_socket.close()

main()
