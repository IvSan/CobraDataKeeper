import json
import random
import socket
import string
import threading
import time

from blockchain.chain import Chain
from network.address import Address


class Peer:
    HOST = '127.0.0.1'
    PORT = 65000

    def __init__(self):
        self.known_peers = []
        self.chain = Chain()

        chain_thread = threading.Thread(target=self.keep_chain, args=())
        chain_thread.start()

        network_listening_thread = threading.Thread(target=self.keep_listening, args=())
        network_listening_thread.start()

    def keep_chain(self):
        while True:
            self.chain.add_block()
            self.chain.store_data(random.choice(string.ascii_letters))
            time.sleep(10)

    def keep_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Peer.HOST, Peer.PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    peer_address = Address(addr[0], addr[1])

                    while True:
                        data_bytes = conn.recv(1024)
                        if not data_bytes:
                            break
                        data = data_bytes.decode()

                        if data == 'status':
                            conn.sendall('ok'.encode())
                        elif data == 'chain':
                            conn.sendall(self.chain.to_json().encode())
                        elif data == 'peers':
                            conn.sendall(self.known_peers_to_json().encode())

                        print('Connected by', peer_address)
                        if peer_address not in self.known_peers:
                            self.known_peers.append(peer_address)
                        print('Known peers:', self.known_peers)

                    conn.close()

    def known_peers_to_json(self):
        return json.dumps(self.known_peers, default=lambda o: o.__dict__, sort_keys=True, indent=4)
