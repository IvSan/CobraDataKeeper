import json
import random
import sched
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

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(60, 1, self.keep_known_peers_clean)
        self.scheduler.run()

    def keep_chain(self):
        while True:
            self.chain.add_block()
            self.chain.store_data(random.choice(string.ascii_letters))

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
                            known_peers_except_requestor = list(
                                filter(lambda p: p != peer_address, self.known_peers))
                            conn.sendall(Peer.peers_to_json(known_peers_except_requestor).encode())

                        print('Connected by', peer_address)
                        if peer_address in self.known_peers:
                            self.known_peers.remove(peer_address)
                        self.known_peers.append(peer_address)
                        print('Known peers:', self.known_peers, '\n')

                    conn.close()

    @staticmethod
    def peers_to_json(known_peers):
        return json.dumps(known_peers, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def keep_known_peers_clean(self):
        for peer_address in self.known_peers:
            if peer_address.updated < time.time() - 3600:
                self.known_peers.remove(peer_address)
        self.scheduler.enter(60, 1, self.keep_known_peers_clean)
