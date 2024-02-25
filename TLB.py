class TLB:
    def __init__(self, size):
        self.size = 16
        self.entries = []

    def lookup(self, logical_page):
        for entry in self.entries:
            if entry[0] == logical_page:
                return entry[1]  # Return the physical frame if the logical page is found
        return None  # Return None if the logical page is not found (TLB miss)
        
    def insert(self, page, frame):
        if self.isFull():
            self.entries.pop(0)  # Remove the oldest entry (FIFO)
        self.entries.append((logical_page, physical_frame))  # Add the new entry to the end

    def isFull(self):
        return len(self.tlb) == self.size 
    
    # def delete(self, frame):
