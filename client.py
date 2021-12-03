import sys
from time import sleep
import socket
import select


if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <server_IP> <server_Port>')
    exit(0)

server_IP = sys.argv[1]
server_port = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((server_IP, server_port))

inputs = [server, sys.stdin]

usr = input('Enter your username: ')
server.send(usr.encode())

while True:
    input_socket, output_socket, error_socket = select.select(inputs, [], [])
    for sock in input_socket:
        if sock == server:
            msg = sock.recv(1024)
            print(msg.decode())
        else:
            msg = input()
            server.send(msg.encode())
            if msg == "exit":
                server.send(msg.encode())
                sleep(0.5)
                server.close()
                print('Disconnect from the chat room!')
                exit(0)