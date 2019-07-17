import random
import string
import threading

from blockchain.chain import Chain


class Peer:

    def __init__(self):
        # try to read from file
        self.chain = Chain()
        chain_thread = threading.Thread(target=self.keep_chain, args=())
        chain_thread.start()

    def keep_chain(self):
        while True:
            self.chain.add_block()
            self.chain.store_data('rnd data: ' + random.choice(string.ascii_letters))
            # save to file
