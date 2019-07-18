import json
import os

from tqdm import tqdm

from blockchain.chain import Chain


class Peer:

    def __init__(self, filename: str = 'chain'):
        self.filename = filename
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
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
            with open(self.filename, "w") as file:
                file.write(self.chain.to_json())
                file.close()
