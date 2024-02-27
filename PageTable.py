class PageTable:

    #2^8 page table entries
    def __init__(self, num_frames):
        self.entries = [] *  256 
        self.size = 256
        self.page_size = 256
        self.num_frames = num_frames
        self.num_pages = 256
        
    def lookup(self, page):
        return self.entries[page] # Return the physical frame if it exists, else None
        
    def insert(self, page, frame):
        if self.entries[page] is not None:
            # do something
            print("Page already exists")
        else:
            self.entries[page] = frame

    def isFull(self):
        return len(self.PageTable) == self.size 
    
    def delete(self, page):
        del self.entries[page]

    def size(self):
        return len(self.entries)
