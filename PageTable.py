class PageTable:

    #2^8 page table entries
    def __init__(self, num_pages, num_frames):
        self.page_size = 256
        self.num_frames = num_frames
        self.num_pages = num_pages
        self.size = 256
        self.entries = {} # List of tuples (page #, frame #)

    def __init__(self):
        self.size = 16
        self.entries ={}  # List of tuples (page #, frame #)

    def lookup(self, page):
        return self.entries.get(page, None) # Return the physical frame if it exists, else None
        
    def insert(self, page, frame):
        if self.isFull():
            self.entries.pop(next(iter(self.entries)))   # Remove the oldest entry (FIFO)
        self.entries[page] = frame  # Add the new entry to the end

    def isFull(self):
        return len(self.tlb) == self.size 
    
    def delete(self, frame):
        for page, frame in self.entries.items():
            if frame == frame:
                self.entries.pop(page)
                break

    def size(self):
        return len(self.entries)
    
    def contains(self, page):
        return page in self.entries
