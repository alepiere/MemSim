# use given algorithm (or FIFO) to replace page in memory
class Memory:
    def __init__(self, frames, alg):
        self.data = [] * frames
        self.pra = alg


