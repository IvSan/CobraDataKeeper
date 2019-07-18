import json
import os

from tqdm import tqdm

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

        self.chain.validate()

    def store_data(self, data) -> None:
        self.chain.store_data(data)

    def keep_chain(self, n: int, verbose: bool):
        for _ in tqdm(range(n)):
            self.chain.add_block(verbose)
            with open("chain.txt", "w") as file:
                file.write(self.chain.to_json())
                file.close()
