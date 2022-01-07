import sys
from time import sleep
import socket
import select
import hashlib
import ssl
from Crypto.Cipher import AES

KEY = hashlib.sha256(b"passwd").digest()

IV = b"abcdefghijklmnop"
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)


if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <server_IP> <server_Port>')
    exit(0)

server_IP = sys.argv[1]
server_port = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_server = ssl.wrap_socket(server, cert_reqs=ssl.CERT_REQUIRED, ca_certs='cert.crt')
ssl_server.connect((server_IP, server_port))

inputs = [ssl_server, sys.stdin]

usr = input('Enter your username: ')
ssl_server.send(usr.encode())

while True:
    input_socket, output_socket, error_socket = select.select(inputs, [], [])
    for sock in input_socket:
        if sock == ssl_server:
            msg = sock.recv(1024)
            print(msg.decode())
        else:
            msg = input()
            ssl_server.send(msg.encode())
            if msg == "exit":
                ssl_server.send(msg.encode())
                sleep(0.5)
                ssl_server.close()
                print('Disconnect from the chat room!')
                exit(0)