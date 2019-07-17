from hashlib import sha256
from time import time


class Block:

    def __init__(self, index=None, close_time=None, data=None, previous_hash=None, proof=None):
        self.index = index if index is not None else 0
        self.time = close_time if close_time is not None else time()
        self.data = data if data is not None else []
        self.previous_hash = previous_hash if previous_hash is not None else 0
        self.proof = proof if proof is not None else '0'

    @classmethod
    def from_json(cls, json_data):
        return Block(index=json_data['index'],
                     close_time=json_data['time'],
                     data=json_data['data'],
                     previous_hash=json_data['previous_hash'],
                     proof=json_data['proof'])

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
