import json
import os
import random
import string
import sys
import threading

from blockchain.chain import Chain


class Peer:

    def __init__(self):
        if os.path.isfile('chain.txt'):
            with open("chain.txt", "r") as file:
                stored_chain = file.read()
                file.close()
            self.chain = Chain.from_json(json.loads(stored_chain))
        else:
            self.chain = Chain()

        if not self.chain.validate():
            print("Invalid chain")
            sys.exit()

        chain_thread = threading.Thread(target=self.keep_chain, args=())
        chain_thread.start()

    def keep_chain(self):
        while True:
            self.chain.add_block()
            self.chain.store_data('rnd data: ' + random.choice(string.ascii_letters))

            with open("chain.txt", "w") as file:
                file.write(self.chain.to_json())
                file.close()

            # add one piece of data and end process
