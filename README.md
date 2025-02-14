# COMP 7005 Assignment 3 - Client/Server Application

## Author:
Matthew Puyat
A01272463
February 14, 2025

## Purpose
This client/server application demonstrates network communication using network sockets. The application uses two sockets (client and server) that communicate over an agreed IP address and port. The client sends a key and the contents of a file to the server, which encrypts the contents using the key and returns the encrypted data to the client. The server has I/O multiplexing abilities, allowing it to handle multiple clients (up to a preset limit of 5).

### Clone the Repository
To obtain the project, clone the GitHub repository:
```bash git clone https://github.com/Matirix/NetworkSocketsMultiplexing.git```

## Running the Application

### Starting the Server
Run the server with the following command:
```bash python3 ./server.py -i <ip_addr> -p <port>```

- `<ip_addr>`: The IP address the server will bind to.
- `<port>`: The port the server will bind to.
- `-e`: Run example with localhost and port set to `3333`.

### Starting the Client
Run the client with the following command:
```bash python3 ./client.py -i <ip_addr> -p <port> -f <filename> -k <key> ```
or
```bash python3 ./client.py -e```

- `<ip_addr>`: The IP address the client will connect to.
- `<port>`: The port the client will connect to.
- `<filename>`: The name of the file the client will send.
- `<key>`: The encryption key the server will use to encrypt the file.
- `-e`: Run example with localhost and port set to `3333`, key `aaaabbb`, and file `hello world zzzzz`.

## Command Line Arguments

### `server.py`
| Variable | Purpose                                         |
|----------|-------------------------------------------------|
| `<ip_addr>` | IP address the server will bind to.            |
| `<port>` | Port the server will bind to.                   |
| `-e` | Example run with localhost `127.0.0.1` and port `3333`. |

### `client.py`
| Variable | Purpose                                         |
|----------|-------------------------------------------------|
| `<ip_addr>` | IP address the client will connect to.        |
| `<port>` | Port the client will connect to.               |
| `<filename>` | The name of the file the client will read.    |
| `<key>` | The encryption key the server will use.        |
| `-e` | Example run with localhost `127.0.0.1` and port `3333`, key `aaaabbb`, and file `hello world zzzzz`. |

## Examples

### Basic Example

```python3 ./server.py 127.0.0.1 3333```				// Localhost and Port
```python3./client.py 127.0.0.1 8080 test1.txt ‘key’```	// name of the file

```python3 ./server.py 192.168.3.1 8080```			// Localhost and Port
```python3 ./client.py 192.168.3.1 8080 test2.txt ‘abc’```	// name of the file


```bash python3 ./server.py 127.0.0.1 3333```
``` bash python3 ./client.py 127.0.0.1 8080 test1.txt ‘key’
& python3./client.py 127.0.0.1 8080 test2.txt ‘key’
& python3 ./client.py 127.0.0.1 8080 test3.txt ‘key’
& python3 ./client.py 127.0.0.1 8080 test4.html ‘key’
& python3 ./client.py 127.0.0.1 8080 test5.txt ‘key’
```
// Concurrently processes 5 test files
