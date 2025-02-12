import socket

def main():
    host = '127.0.0.1'
    port = 3333
    print("Server listening on Address", host, " and port: ", port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen() # listen for x many connections
    connection, address = server_socket.accept()
    print("Connection from: ", str(address))
    while True:
        data = connection.recv(1024).decode()
        if not data:
            break
        print("From connected user: ", data)
        connection.send(data.encode())

    connection.close()

main()
