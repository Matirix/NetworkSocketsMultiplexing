import socket

def main():
    host = '127.0.0.1'
    port = 3333
    print("Server listening on Address", host, " and port: ", port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    message = "Hello"
    # Sending
    server_socket.send(message.encode())

    # Received
    data = server_socket.recv(1024).decode()
    print("Received from server: ", data)

    server_socket.close()

main()
