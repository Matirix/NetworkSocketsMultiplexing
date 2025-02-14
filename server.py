from typing import Optional
import socket
from curses.ascii import isalpha, isupper
import enum
import argparse
from time import sleep
import threading
import select
from helper import is_valid_address_port as ip_and_port_validator


class ServerState(enum.Enum):
    INIT = 0
    LISTENING = 1
    CONNECTED = 2
    RECEIVING = 3
    DECRYPTING = 4
    SENDING = 5
    CLOSING = 6

def parse_arguments():
    """
    Parses command line arguments for Creating a Server Connection
    :return: ip, port
    """
    parser = argparse.ArgumentParser(description="Client-Server Model that uses Select for I/O Multiplexing")
    parser.add_argument("-i","--ip", type=str, help="Host IP Address")
    parser.add_argument("-p","--port", type=int, help="Host Port Number")
    parser.add_argument('-e', "--example", action='store_true', help="Shows example usage on fixed host and port")
    args = parser.parse_args()
    if args.example:
        ip, port = '127.0.0.1', 3333
        example_socket = ServerSocket(ip, port)
        example_socket.listening_multiple_connections()
    try:
        ip = args.ip if ip_and_port_validator(args.ip, False) else ""
        port = args.port if ip_and_port_validator(args.port, True) else ""
    except Exception as e:
        print("Parse Error -", e)
        exit(1)

    return ip, port


class ServerSocket:
    def __init__(self, server_ip, server_port):
        """
        Constructor for ServerSocket
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.state = ServerState.INIT
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_list = [self.server_socket]
        self.binding()

    def binding(self):
        """
        Binds the ServerSocket to the IP and Port - Allowd for address reuse
        """
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_ip, self.server_port))


    def listening_multiple_connections(self):
        """
        Listens for multiple connections up to 5 clients and handles them in separate threads.
        Uses mutex to lock the critical section of the code AKA the socket list
        Uses Select to monitor the sockets for read, write and exception events
        """
        self.server_socket.listen(5)
        self.state = ServerState.LISTENING
        print(f"Monitoring Sockets on {self.server_ip}:{self.server_port}")
        while True:
            try:
                with self.lock:
                    read_sockets, _, exception_list = select.select(self.socket_list, [], self.socket_list)
                for sock in read_sockets:
                    if sock == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        self.socket_list.append(client_socket)
                        self.state = ServerState.CONNECTED
                        threading.Thread(target=self.receive_connection, args=(client_socket,)).start()
                for sock in exception_list:
                    self.remove_socket_safely(sock)
            except Exception as e:
                print("Error handling socket:", e)
            except KeyboardInterrupt as e:
                print("Command/Ctrl +C Detected \n Closing Server", e )
                self.remove_socket_safely(self.server_socket)
                self.state = ServerState.CLOSING
                exit(1)

    def receive_connection(self, sock):
        """
        Handles the connection with the client
        """
        try:
            data = sock.recv(1024).decode()
            if not data:
                raise Exception("Client Disconnected")
            payload = self.process_data(data)
            if payload:
                sock.send(payload.encode())
        except Exception as e:
            print("Connection Error", e)
        finally:
            self.remove_socket_safely(sock)


    def process_data(self, data):
        """
        Processes the data received from the client
        """
        if self.state == ServerState.CONNECTED:
            self.state = ServerState.RECEIVING
            text, key = data.split("&", 1)
            print(f"====Thread: {threading.get_ident()}=====")
            print(f"Decrpyting {text} with key {key}")
            print("==========================")
            payload = self.decrypt_viegenere_cipher(text, key)
            print(f"=====Finished Decrypting {threading.get_ident()}======")
            return payload
        # else:
            # print(f"Server state = {self.state}")


    def remove_socket_safely(self, sock):
        """
        Safely removes the client socket from the socket list using lock
        """
        with self.lock:
            if sock in self.socket_list:
                self.socket_list.remove(sock)
        sock.close()


    def decrypt_viegenere_cipher(self, message, key) -> str:
        """
        Decrypts the message using the Vigenere Cipher
        """
        self.state = ServerState.DECRYPTING
        decoded_string = str()
        key_length = len(key)
        for i in range(len(message)):
            letter = message[i]
            shift = ord(key[i % key_length]) - ord('a')
            if letter == ' ' or not isalpha(letter):
                decoded_string += letter
                print(f"Thread: {threading.get_ident()} - Ignoring Special Chracter: {letter}")
                continue
            if isupper(letter):
                decoded_char = chr(((ord(letter) - ord('A') - shift) % 26) + ord('A'))
            else:
                decoded_char = chr(((ord(letter) - ord('a') - shift) % 26) + ord('a'))
            decoded_string += decoded_char
            print(f"Thread: {threading.get_ident()} - DECODED CHARACTER: {decoded_char}")
            sleep(0.5)
        return decoded_string


if __name__ == '__main__':
    host, port = parse_arguments()
    ss = ServerSocket(host, port)
    ss.listening_multiple_connections()
