from hashlib import sha256
from time import time


class Block:

    def __init__(self, index, previous_hash, proof):
        self.index = index
        self.time = time()
        self.data = []
        self.previous_hash = previous_hash
        self.proof = proof

    def store_data(self, data):
        self.data.append(data)

    def hash(self):
        h = sha256()
        h.update(
            str(self.index).encode('utf-8') +
            str(self.time).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.proof).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block index: " + str(self.index) + \
               "\nBlock date: " + str(self.time) + \
               "\nBlock data: " + str(self.data) + \
               "\nCurrent block hash: " + str(self.hash()) + \
               "\nPrevious block hash: " + str(self.previous_hash) + \
               "\nProof: " + str(self.proof) + \
               "\n--------------\n"
