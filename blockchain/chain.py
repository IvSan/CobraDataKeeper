import json
from hashlib import sha256
from uuid import uuid4

from blockchain.block import Block


class Chain:
    DIFFICULTY = 20
    TARGET = 2 ** (256 - DIFFICULTY)

    def __init__(self, chain=None, current_data=None):
        self.chain = chain if chain is not None else [Block()]
        self.current_data = current_data if current_data is not None else []

    @classmethod
    def from_json(cls, json_data):
        chain = []
        for block_data in json_data['chain']:
            chain.append(Block.from_json(block_data))
        return Chain(chain=chain, current_data=json_data['current_data'])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def store_data(self, data) -> None:
        self.chain[-1].store_data(data)

    def add_block(self, verbose: bool) -> None:
        index = len(self.chain)
        previous_block_hash = self.chain[-1].hash()
        proof, tries = self.find_proof()

        block = Block(index=index, previous_hash=previous_block_hash, proof=proof)
        self.chain.append(block)

        if not self.validate():
            raise Exception("Invalid chain")
        if verbose:
            print(f'Block has been closed with work amount of: {str(tries)}')
            print(self.chain[-2])

    def find_proof(self) -> (str, int):
        tries = 0
        while True:
            tries += 1
            proof = str(uuid4())
            hash_to_check = sha256()
            hash_to_check.update(self.chain[-1].hash().encode() + proof.encode())
            if int(hash_to_check.hexdigest(), 16) <= Chain.TARGET:
                return proof, tries

    def validate(self) -> bool:
        if len(self.chain) < 2:
            return True
        for i, block in enumerate(self.chain[:1]):
            hash_to_check = sha256()
            hash_to_check.update(block.hash().encode() + self.chain[i + 1].proof.encode())
            if int(hash_to_check.hexdigest(), 16) > Chain.TARGET:
                return False
        return True

    def __repr__(self) -> str:
        result = ''
        for item in self.chain:
            result += '\n' + str(item)
        return result
