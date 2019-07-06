import socket

from blockchain.chain import Chain

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall('chain'.encode())
    data = s.recv(99999999).decode()

chain = Chain(json_data=data)
print('Received:', chain)
