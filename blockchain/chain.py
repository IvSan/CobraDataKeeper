from hashlib import sha256
from uuid import uuid4

from blockchain.block import Block


class Chain:
    DIFFICULTY = 20
    TARGET = 2 ** (256 - DIFFICULTY)

    def __init__(self):
        self.current_data = []
        self.chain = []

    def add_block(self):
        index = len(self.chain)
        previous_block_hash = self.chain[-1].hash() if self.chain else 0
        proof = Chain.find_proof(self.chain[-1]) if self.chain else 0

        block = Block(index, previous_block_hash, proof)
        self.chain.append(block)

    @staticmethod
    def find_proof(last_block):
        while True:
            proof = str(uuid4())
            hash_to_check = sha256()
            hash_to_check.update(last_block.hash().encode() + proof.encode())
            if int(hash_to_check.hexdigest(), 16) <= Chain.TARGET:
                return proof

    def __str__(self):
        result = ''
        for item in self.chain:
            result += '\n\n' + str(item)
        return result


chain = Chain()
chain.add_block()
chain.add_block()
chain.add_block()
print(chain)
