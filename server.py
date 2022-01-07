import sys
import socket
import threading
import ssl

keyFile = "priv.pem"
certFile = "cert.crt"

client_list = []

def clients(connection, addr):
    usr = connection.recv(1024).decode()
    usr_addr = f'{usr}@{addr[0]}:{addr[1]}'
    print(f'{usr_addr} connected!')
    connection.send(f'\033[7mWelcome {usr}!\033[0m'.encode())
    broadcast(connection, f'\033[91m[SYSTEM]\033[0m {usr} connected!')
    while True:
        msg = connection.recv(1024).decode()
        if msg == "exit" or msg == "exitexit" or msg == "":
            print(f'{usr_addr} disconnected!')
            broadcast(connection, f'\033[91m[SYSTEM]\033[0m {usr} disconnected!')
            disconnect(connection)
            break
        print(f'{usr_addr}: {msg}')
        msg = usr + ": " + msg
        broadcast(connection, msg)

def broadcast(connection, msg):
    for client in client_list:
        if client != connection:
            try:
                client.send(msg.encode())
            except:
                client.close()
                client_list.remove(client)

def disconnect(connection):
    if connection in client_list:
        client_list.remove(connection)

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <server_IP> <server_Port>')
    exit(0)

server_IP = sys.argv[1]
server_port = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.bind((server_IP, server_port))
server.listen(255)
ssl_server = ssl.wrap_socket(server, keyfile=keyFile, certfile=certFile, server_side=True)

while True:
    connection, addr = ssl_server.accept()
    client_list.append(connection)
    client = threading.Thread(target=clients, args=(connection, addr))
    client.start()