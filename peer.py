import json
import os
import sys

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

    def store_data(self, data) -> None:
        self.chain.store_data(data)

    def keep_chain(self, n):
        for i in range(n):
            self.chain.add_block()
            with open("chain.txt", "w") as file:
                file.write(self.chain.to_json())
                file.close()

            # add one piece of data and end process
