from queue import Queue


class TLB:
    def __init__(self):
        self.size = 16
        self.entries ={}  # List of tuples (page #, frame #)
        self.reference_Queue = Queue()


    def lookup(self, page):
        return self.entries.get(page, None) # Return the physical frame if it exists, else None
        
    def insert(self, page, frame):
        if self.isFull():
            self.entries.pop(self.reference_Queue.get())
        self.reference_Queue.put(page)
        self.entries[page] = frame  # Add the new entry to the end

    def isFull(self):
        return len(self.entries) == self.size 

    def size(self):
        return len(self.entries)
    
    def contains(self, page):
        return page in self.entries

    def printTable(self):
        print(self.entries)