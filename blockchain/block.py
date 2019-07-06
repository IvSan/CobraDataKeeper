from hashlib import sha256
from time import time


class Block:

    def __init__(self, index=None, previous_hash=None, proof=None, json_data=None):
        if not json_data:
            self.index = index
            self.time = time()
            self.data = []
            self.previous_hash = previous_hash
            self.proof = proof
        else:
            self.index = json_data['index']
            self.time = json_data['time']
            self.data = json_data['data']
            self.previous_hash = json_data['previous_hash']
            self.proof = json_data['proof']

    def store_data(self, data) -> None:
        self.data.append(data)

    def hash(self) -> str:
        h = sha256()
        h.update(
            str(self.index).encode('utf-8') +
            str(self.time).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.proof).encode('utf-8')
        )
        return h.hexdigest()

    def __repr__(self) -> str:
        return 'Block index: ' + str(self.index) + \
               '\nBlock date: ' + str(self.time) + \
               '\nBlock data: [' + ' '.join(str(d) for d in self.data) + ']' + \
               '\nPrevious block hash: ' + str(self.previous_hash) + \
               '\nProof: ' + str(self.proof) + \
               '\nCurrent block hash: ' + str(self.hash()) + \
               '\n'
