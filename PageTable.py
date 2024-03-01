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
        else:
            self.reference_Queue.put(page)


    def getVictim(self, page_numbers, index, opt_set):
        if self.pra == 'FIFO' or self.pra == 'LRU':
            victim = self.reference_Queue.get()
        else:
            #check every loaded in frame to see which one will be used further in the future for OPT
            for key in opt_set:
                distance = 0
                for page_num in page_numbers[index:]:
                    if key == page_num:
                        opt_set[key] = distance
                        break
                    distance += 1
                #apparently you can make an else statement to run if for loop doesnt exit with a break
                else:
                    opt_set[key] = distance
            victim = max(opt_set, key=opt_set.get)
        return victim

    def isFull(self):
        return len(self.PageTable) == self.size 

    def size(self):
        return len(self.entries)

    def printTable(self):
        print(self.entries)