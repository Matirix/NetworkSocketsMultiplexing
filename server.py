from typing import Optional
import socket
import sys
from curses.ascii import isalpha, isupper
import enum
from time import sleep
import threading
import select


class ServerState(enum.Enum):
    INIT = 0
    LISTENING = 1
    CONNECTED = 2
    RECEIVING = 3
    DECRYPTING = 4
    SENDING = 5
    CLOSING = 6


class ServerSocket:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.state = ServerState.INIT
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_list = [self.server_socket]
        self.binding()

    def binding(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_ip, self.server_port))

    def listening(self):
        self.server_socket.listen()
        self.state = ServerState.LISTENING
        print("Server is listening")
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.state = ServerState.CONNECTED
                data = client_socket.recv(1024).decode()
                payload:str = self.process_data(data)
                client_socket.send(payload.encode())
                client_socket.close()
            except KeyboardInterrupt as e:
                print("Command/Ctrl +C Detected \n Closing Server", e )
                break
        self.server_socket.close()

    def handle_connection(self, sock):
        try:
            data = sock.recv(1024).decode()
            if not data:
                raise Exception("Client Disconnected")
            payload: str = self.process_data(data)
            sock.send(payload.encode())
        except Exception as e:
            print("Connection Error", e)
        finally:
            self.remove_socket_safely(sock)
            sock.close()

    def remove_socket_safely(self, client_socket):
        with self.lock:
            if client_socket in self.socket_list:
                self.socket_list.remove(client_socket)


    def listening_multiple_connections(self):
        self.server_socket.listen(5)
        self.state = ServerState.LISTENING
        # TODO add a time out
        print("Monitoring Server Socket")
        while True:
            try:
                with self.lock:
                    read_sockets, _, exception_list = select.select(self.socket_list, [], self.socket_list)
                for sock in read_sockets:
                    if sock == self.server_socket:
                        client_socket, client_address = self.server_socket.accept()
                        self.socket_list.append(client_socket)
                        self.state = ServerState.CONNECTED
                        threading.Thread(target=self.handle_connection, args=(client_socket,)).start()
                for sock in exception_list:
                    self.remove_socket_safely(sock)
                    sock.close()
            except Exception as e:
                print("Error handling socket:", e)


    def process_data(self, data:str) -> Optional[str]:
        if self.state == ServerState.CONNECTED:
            self.state = ServerState.RECEIVING
            print("Recieved Data:", data)
            text, key = data.split("&", 1)
            payload = self.decrypt_viegenere_cipher(text, key)
            return payload
        else:
            print(f"Server state = {self.state}")


    def decrypt_viegenere_cipher(self, message, key, decrypt=True) -> str:
        self.state = ServerState.DECRYPTING
        encoded_string = str()
        key_length = len(key)
        for i in range(len(message)):
            letter = message[i]
            if letter == ' ' or not isalpha(letter):
                encoded_string += letter
                continue
            if isupper(letter):
                shift = ord(key[i % key_length]) - ord('A')
                encoded_char = chr(((ord(letter) - ord('A') + shift) % 26) + ord('A'))
            else:
                shift = ord(key[i % key_length]) - ord('a')
                encoded_char = chr(((ord(letter) - ord('a') + shift) % 26) + ord('a'))
            encoded_string += encoded_char
            print(encoded_char)
            sleep(0.5)
        return encoded_string


def main():
    host = '127.0.0.1'
    port = 3333
    ss = ServerSocket(host, port)
    ss.listening_multiple_connections()

main()
