import json
from hashlib import sha256
from uuid import uuid4

from blockchain.block import Block


class Chain:
    DIFFICULTY = 22
    TARGET = 2 ** (256 - DIFFICULTY)

    def __init__(self, json_data=None):
        if json_data:
            deserialized = json.loads(json_data)
            self.chain = []
            for block_data in deserialized['chain']:
                self.chain.append(Block(json_data=block_data))
        else:
            self.current_data = []
            genesis = Block(0, 0, 0)
            self.chain = [genesis]

    def add_block(self) -> None:
        index = len(self.chain)
        previous_block_hash = self.chain[-1].hash()
        proof, tries = self.find_proof()

        block = Block(index, previous_block_hash, proof)
        self.chain.append(block)

        if not self.validate():
            raise Exception("Invalid chain")
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
        for i, block in enumerate(self.chain[:1]):
            hash_to_check = sha256()
            hash_to_check.update(block.hash().encode() + self.chain[i + 1].proof.encode())
            if int(hash_to_check.hexdigest(), 16) > Chain.TARGET:
                return False
        return True

    def store_data(self, data) -> None:
        self.chain[-1].store_data(data)

    def __repr__(self) -> str:
        result = ''
        for item in self.chain:
            result += '\n' + str(item)
        return result

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
