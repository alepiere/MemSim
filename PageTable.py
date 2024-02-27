from queue import Queue

class PageTable:

    #2^8 page table entries
    def __init__(self, num_frames, pra):
        self.entries = [None] * 256 
        self.size = 256
        self.page_size = 256
        self.num_frames = num_frames
        self.num_pages = 256
        self.reference_Queue = Queue()
        self.pra = pra
        
    def lookup(self, page):
        return self.entries[page] # Return the physical frame if it exists, else None
        
    def update(self, page, frame):
        self.entries[page] = frame
        # if self.entries[page] is None:
        #     self.entries[page] = frame
        #     self.reference_Queue.put(page)
        # else:
        #     victim = self.reference_Queue.get()
        #     self.entries.pop(victim)
        #     self.entries[page] = frame
        #     for item in self.reference_Queue.queue:
        #         if item == victim:
        #             if self.pra == 'LRU':
        #                 self.reference_Queue.get(item)
        #                 self.reference_Queue.put(item)     

    def updateReferenceQueue(self, page):
        #not an eloquent if statement maybe can be made cleaner
        if self.reference_Queue.empty():
            self.reference_Queue.put(page)
        for item in self.reference_Queue.queue:
                 if item == page:
                     if self.pra == 'LRU':
                         #look through all the items in reference queue and put page to front
                         #if it is already found to indicate if it has been used recently
                         self.reference_Queue.get(item)
                         self.reference_Queue.put(item) 
                         break 
                         #do nothing if it is FIFO because it is already in position it should be for replacement order

    def getVictim(self):
        victim = self.reference_Queue.get()
        #self.entries[victim] = None
        return victim

    def isFull(self):
        return len(self.PageTable) == self.size 

    def size(self):
        return len(self.entries)

    def printTable(self):
        print(self.entries)