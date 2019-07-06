from time import time


class Note:

    def __init__(self, data):
        self.time = time()
        self.data = data

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return str(self.data)
