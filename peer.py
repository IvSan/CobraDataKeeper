import threading

from blockchain.chain import Chain


class Peer:

    def __init__(self):
        self.chain = Chain()
        chain_thread = threading.Thread(target=self.keep_chain, args=())
        chain_thread.start()

    def keep_chain(self):
        while True:
            self.chain.add_block()
