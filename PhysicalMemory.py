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
            #print("Use page replacement algorithm")
            return None
        
    # def addFrame(self, frame, data):
    #     index = self.findFreeFrame()
    #     if index is None:
    #         # find victim
    #         print("victim")
    #         victim = PageTable.
    #         self.updateFrame(victim, data)
    #     else:
    #         self.data[index] = data
    #         self.size += 1

    def getFrameData(self, frame):
        return self.data[frame]
    
    def updateFrame(self, frame, data):
        self.data[frame] = data
