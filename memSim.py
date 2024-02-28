import sys
import argparse
from TLB import TLB
from PageTable import PageTable
from PhysicalMemory import Memory

# usage: memSim <reference-sequence-file.txt> <FRAMES> <PRA>


def getPageData(page_number):
    backing_storage = open("BACKING_STORE.bin", 'rb')
    offset = page_number * 256
    backing_storage.seek(offset)
    page_content = backing_storage.read(256)
    return page_content

def print_stats(translatedAddr, pagefaults, hits, misses):
    print("Number of Translated Addresses = %d" % len(translatedAddr))
    print("Page Faults = %d" % pagefaults)
    print("Page Fault Rate = %.3f" % (pagefaults/(hits+misses)))
    print("TLB Hits = %d" % hits)
    print("TLB Misses = %d" % misses)
    print("TLB Hit Rate = %.3f" % (hits/(hits+misses)))

def handlePageFault(page_number, memory, page_table, page_numbers, index, opt_set):
    #get data to be inserted into replaced frame
    frame_data = getPageData(page_number)
    #find the next frame number index to replace
    frame_number = memory.findFreeFrame()
    if frame_number is None:
        # if there isnt an open index in physical memory, find page to replace
        victim = page_table.getVictim(page_numbers, index, opt_set)
        # keep index of the victim to know where to set new page table entry
        frame_number = page_table.entries[victim]
        # set loaded bit to None in page table (none is not loaded)
        page_table.update(victim, None)
        del opt_set[victim]
        # update new page table entry with index you are replacing
        page_table.update(page_number, frame_number)
        opt_set[page_number] = 0
        # update the frame in physical memory
        memory.updateFrame(frame_number, frame_data)
    else:
        page_table.update(page_number, frame_number)
        opt_set[page_number] = 0
    return frame_data

def addressesToPageNumbers(addresses):
    page_numbers = []
    for address in addresses:
        page_number = format(address, '016b')
        page_numbers.append(int(page_number[0:8], 2))
    return page_numbers

def main():
    parser = argparse.ArgumentParser(prog='MemSim', description='Simulate memory management')
    parser.add_argument('filename', help='Path to the input file')
    parser.add_argument('frames', nargs='?', type=int, default=256, help='Number of frames in the system')
    parser.add_argument('pra', nargs='?', choices=['FIFO', 'LRU', 'OPT'], default='FIFO', help='Page replacement algorithm')
    args = parser.parse_args()

    tlb = TLB()
    page_table = PageTable(num_frames = args.frames, pra = args.pra)
    memory = Memory(frames=args.frames, pra=args.pra.upper())
    opt_set = {}

    reference_file = open(args.filename, 'r')
    virtual_addresses = [int(line.strip()) for line in reference_file]
    page_numbers = addressesToPageNumbers(virtual_addresses)

    pagefaults = 0
    hits = 0
    misses = 0

    #enumerate to get index in case of the OPT page replacement algorithim
    for index, address in enumerate(virtual_addresses):
        binary_string = format(address, '016b')
        page_number = int(binary_string[0:8], 2)
        page_offset = int(binary_string[8:], 2)

        # print(page_number, page_offset, '\n')

        frame_number = tlb.lookup(page_number)
        # tlb.printTable()
        # if page in TBL, increment TLB hits if page still valid
        if frame_number is not None:
            #check if the tlb entry is valid
            if page_table.lookup(page_number) is None:
                frame_data = handlePageFault(page_number, memory, page_table, page_numbers, index, opt_set)
                pagefaults += 1
                misses+=1
                if args.pra != 'OPT':
                    page_table.updateReferenceQueue(page_number)
            else:
                hits += 1
                frame_data = memory.getFrameData(frame_number)
        else: 
            misses += 1
            frame_number = page_table.lookup(page_number)
            if frame_number is not None:
                # get frame data from page table
                frame_data = memory.getFrameData(frame_number) 
            else:
                #no frame number returned = page fault so handle that accordingly
                frame_data = handlePageFault(page_number, memory, page_table, page_numbers, index, opt_set)
                #get updated frame number from page table after page fault is resolved
                frame_number = page_table.lookup(page_number)
                #extract value using the offset inside the physical memory
                data_value = frame_data[page_offset:page_offset+1]
                pagefaults += 1
                #only update TLB if page is not already in TLB
                tlb.insert(page_number, frame_number)
            #update reference queue with the page number that was accessed/added if not OPT
            if args.pra != 'OPT':
                page_table.updateReferenceQueue(page_number)
        print("{}, {}, {}, {}".format(address, int.from_bytes(data_value, byteorder='big', signed=True), frame_number, frame_data.hex().upper()))
        # print(page_number, " is page number for address ", address)
        # print(int.from_bytes(data_value))
        
    print_stats(virtual_addresses, pagefaults, hits, misses)

if __name__ == '__main__':
    main()