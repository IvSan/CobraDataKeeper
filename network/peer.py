import socket
import threading
import time

from blockchain.chain import Chain


class Peer:
    HOST = '127.0.0.1'
    PORT = 65000

    def __init__(self):
        self.chain = Chain()

        chain_thread = threading.Thread(target=self.keep_chain, args=())
        chain_thread.start()

        network_listening_thread = threading.Thread(target=self.keep_listening, args=())
        network_listening_thread.start()

    def keep_chain(self):
        while True:
            self.chain.add_block()
            time.sleep(3)

    def keep_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Peer.HOST, Peer.PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        print('Received: ', data.decode())
                        conn.sendall(self.chain.to_json().encode())
