import json
import socket

from blockchain.chain import Chain
from network.address import Address

LOCAL = '127.0.0.1'
HOST = '80.211.52.223'  # The server's hostname or IP address
PORT = 65000  # The port used by the server


def request(command: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind((LOCAL, PORT + 1))
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        data = s.recv(99999999).decode()
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return data


chain = Chain(json_data=request('chain'))
chain.validate()
print('Received:', chain)

peers = []
for address_data in json.loads(request('peers')):
    peers.append(Address(json_data=address_data))
print('Known peers:', peers)
