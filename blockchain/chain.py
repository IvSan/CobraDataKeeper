from hashlib import sha256
from uuid import uuid4

from blockchain.block import Block


class Chain:
    DIFFICULTY = 20
    TARGET = 2 ** (256 - DIFFICULTY)
    MAX_NONCE = 2 ** 32

    def __init__(self):
        self.current_data = []
        self.chain = []

    def add_block(self):
        block = Block(len(self.chain),
                      self.chain[-1].hash() if self.chain else sha256(str(uuid4()).encode()).hexdigest(),
                      self.find_proof())
        self.chain.append(block)

    def find_proof(self):
        proof = 0

        if not self.chain:
            return proof

        last_block = self.chain[-1]

        for n in range(Chain.MAX_NONCE):
            hash_to_check = sha256()
            hash_to_check.update(last_block.hash().encode() + str(proof).encode())
            if int(hash_to_check.hexdigest(), 16) <= Chain.TARGET:
                return proof
            else:
                proof += 1
        return '9999'

    def __str__(self):
        result = ''
        for item in self.chain:
            result += str(item)
        return result


chain = Chain()
chain.add_block()
chain.add_block()
chain.add_block()
print(chain)
