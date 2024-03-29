# use given algorithm (or FIFO) to replace page in memory
import PageTable

class Memory:
    def __init__(self, frames, pra):
        self.data = [None for _ in range(frames)]
        self.pra = pra
        self.size = 0
        self.frames = frames

    def findFreeFrame(self):
        if self.size < self.frames:
            #increment size and then return old value (maybe rework this logic)
            self.size += 1
            return (self.size - 1)
        else:
            return None

    def getFrameData(self, frame):
        return self.data[frame]
    
    def updateFrame(self, frame, data):
        self.data[frame] = data

    def printMemory(self):
        print(self.data)