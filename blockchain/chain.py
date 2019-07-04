import json
from hashlib import sha256
from uuid import uuid4

from blockchain.block import Block


class Chain:
    DIFFICULTY = 10
    TARGET = 2 ** (256 - DIFFICULTY)

    def __init__(self):
        self.current_data = []
        genesis = Block(0, 0, 0)
        self.chain = [genesis]

    def add_block(self):
        index = len(self.chain)
        previous_block_hash = self.chain[-1].hash()
        proof, tries = Chain.find_proof(self.chain[-1])

        block = Block(index, previous_block_hash, proof)
        self.chain.append(block)
        print(f'Block has been closed with work amount of: {str(tries)}')
        print(self.chain[-2], '\n\n')

    @staticmethod
    def find_proof(last_block):
        tries = 0
        while True:
            tries += 1
            proof = str(uuid4())
            hash_to_check = sha256()
            hash_to_check.update(last_block.hash().encode() + proof.encode())
            if int(hash_to_check.hexdigest(), 16) <= Chain.TARGET:
                return proof, tries

    def store_data(self, data):
        self.chain[-1].store_data(data)

    def __str__(self):
        result = ''
        for item in self.chain:
            result += '\n\n' + str(item)
        return result

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
