from time import time


class Note:

    def __init__(self, data):
        self.time = time()
        self.data = data

    def __str__(self) -> str:
        return str(self.data)
