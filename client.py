import socket
from enum import Enum
from helper import is_valid_address_port as ip_and_port_validator, validate_key, read_file
import argparse

class ClientState(Enum):
    INIT = 0
    CONNECTING = 1
    CONNECTED = 2
    SENDING = 3
    RECEIVING = 4
    DISCONNECTED = 5


def parse_arguments():
    """
    Parses command line arguments for Client
    :return: ip, port, key, file
    """
    parser = argparse.ArgumentParser(description="Client-Server Model that uses Select for I/O Multiplexing\n")
    parser.add_argument("-i","--ip", type=str, help="Host IP Address")
    parser.add_argument("-p","--port", type=int, help="Host Port Number")
    parser.add_argument('-k', "--key", type=str, help="Key for decryption")
    parser.add_argument('-f', "--file", type=str, help="File to be decoded")
    parser.add_argument('-e', "--example", action='store_true', help="Shows example usage on fixed host and port")
    args = parser.parse_args()

    if args.example:
        ip, port, message, key = '127.0.0.1', 3333, "Hello world zzzz", "aaabbb"
        example_socket = ClientSocket(ip, port, message, key)
        example_socket.connect()
        exit(1)
    try:
        ip = args.ip if ip_and_port_validator(args.ip, False) else ""
        port = args.port if ip_and_port_validator(args.port, True) else ""
        key = args.key if validate_key(args.key) else ""
        message = read_file(args.file)
    except Exception as e:
        print("Parse Error -", e)
        exit(1)

    return ip, port, message, key


class ClientSocket:
    def __init__(self, host_ip: str, host_port, message, key:str):
        """
        Constructor for ClientSocket
        :param host_ip: Host IP Address
        :param host_port: Host Port Number
        :param message: Message to be sent
        :param key: Key for decryption
        """
        self.host_ip = host_ip
        self.host_port = host_port
        self.message = message
        self.key = key
        self.state = ClientState.INIT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def format_payload(self):
        """
        Formats the message and key into a single payload
        """
        return self.message.strip() + '&' + self.key.strip()

    def connect(self):
        """
        Connects to the Server
        """
        self.state = ClientState.CONNECTING
        try:
            self.client_socket.connect((self.host_ip, self.host_port))
            self.state = ClientState.CONNECTED
            self.send_data()
        except Exception as e:
            print("Connection Failed:", e)
            self.state=ClientState.DISCONNECTED

    def send_data(self):
        """
        Sends the message and key to the Server
        """
        if self.state == ClientState.CONNECTED:
            payload = self.format_payload()
            try:
                self.client_socket.send(payload.encode())
                self.state = ClientState.SENDING
                self.await_response()
            except Exception as e:
                print("Sending Error:", e)

    def await_response(self):
        """
        Listens for a response from the Server and then closes the connection
        """
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


if __name__ == '__main__':
    host, port, message, key = parse_arguments()
    client_socket = ClientSocket(host, port, message, key)
    client_socket.connect()
