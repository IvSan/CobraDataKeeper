import json
import sched
import socket
import threading
import time

from blockchain.chain import Chain
from network.address import Address


class Peer:
    PORT = 65000

    def __init__(self):
        self.known_peers = [Address('80.211.52.223', Peer.PORT)]
        self.chain = self.get_chain_from_network()

        chain_thread = threading.Thread(target=self.keep_chain, args=())
        chain_thread.start()

        network_listening_thread = threading.Thread(target=self.keep_listening, args=())
        network_listening_thread.start()

        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(60, 1, self.keep_known_peers_clean)
        self.scheduler.run()

    def get_chain_from_network(self) -> Chain:
        longest_chain = Chain()
        for peer_address in self.known_peers:
            chain = Chain(json_data=Peer.request(peer_address.host, peer_address.port, 'chain'))
            if chain.validate() and len(chain.chain) > len(longest_chain.chain):
                longest_chain = chain
        return longest_chain

    def keep_chain(self):
        while True:
            self.chain.add_block()
            for peer_address in self.known_peers:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.connect((peer_address.host, peer_address.port))
                    s.sendall(('newBlock' + self.chain.to_json()).encode())
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()

    def keep_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', Peer.PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    peer_address = Address(addr[0], Peer.PORT)

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
                        elif data.startswith('newBlock'):
                            chain = Chain(json_data=data[8:])
                            if chain.validate():
                                chain.chain[-1].data.extend(self.chain.chain[-1].data)
                                self.chain = chain
                            print('Block has been received from network')
                            print(self.chain.chain[-1])

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

    @staticmethod
    def request(host: str, port: int, command: str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((host, port))
            s.sendall(command.encode())
            data = s.recv(9999999999).decode()
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            return data
