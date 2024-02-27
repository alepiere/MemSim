class Memory:
    def __init__(self, frames, alg):
        self.data = []
        self.size = 256 * frames
        self.pra = alg

    def 