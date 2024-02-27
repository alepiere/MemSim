import sys
import argparse
from TLB import TLB
from PageTable import PageTable
from PhysicalMemory import Memory

# usage: memSim <reference-sequence-file.txt> <FRAMES> <PRA>


def pageFaultHandler(page_number):
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

def main():
    parser = argparse.ArgumentParser(prog='MemSim', description='Simulate memory management')
    parser.add_argument('filename', help='Path to the input file')
    parser.add_argument('--frames', type=int, default=256, help='Number of frames in the system')
    parser.add_argument('--pra', choices=['FIFO', 'LRU', 'OPT'], default='FIFO', help='Page replacement algorithm')
    args = parser.parse_args()

    tlb = TLB()
    page_table = PageTable(num_frames = args.frames, pra = args.pra)
    memory = Memory(frames=args.frames, pra=args.pra.upper())

    pagefaults = 0
    hits = 0
    misses = 0

    reference_file = open(args.filename, 'r')
    virtual_addresses = [int(line.strip()) for line in reference_file]
    for address in virtual_addresses:
        binary_string = format(address, '016b')
        page_number = int(binary_string[0:8], 2)
        page_offset = int(binary_string[8:], 2)

        print(page_number, page_offset, '\n')

        frame_number = tlb.lookup(page_number)
        # if page in TBL, increment TLB hits
        if frame_number is not None:
            hits += 1
            frame_data = memory.get_frame_data(frame_number)
            #data_value = frame_data[page_offset:page_offset+1] get data value at end of if statement
        else: 
            misses += 1
            page_table.printTable()
            frame_number = page_table.lookup(page_number)
            if frame_number is not None:
                # get frame from page table
                frame_data = memory.getFrameData(frame_number) 
                #data_value = frame_data[page_offset:page_offset+1] dont need here and put on bottom
            else:
                frame_data = pageFaultHandler(page_number)
                nextIndex = memory.findFreeFrame()
                if nextIndex is None:
                    # if there isnt an open index in physical memory, find page to replace
                    victim = page_table.getVictim()
                    # keep index of the victim to know where to set new page table entry
                    nextIndex = page_table.entries[victim]
                    # set loaded bit to None in page table (none is not loaded)
                    page_table.update(victim, None)
                    # update new page table entry with index you are replacing
                    page_table.update(page_number, nextIndex)
                    # update the frame in physical memory
                    memory.updateFrame(nextIndex, frame_data)
                    #print(frame_data)
                else:
                    page_table.update(page_number, nextIndex)
                data_value = frame_data[page_offset:page_offset+1]
                pagefaults += 1
                # go into back storage and get the page
            #update reference queue with the page number that was accessed/added
            page_table.updateReferenceQueue(page_number)
        print(page_number, " is page number for address ", address)
        print(int.from_bytes(data_value))
        
    print_stats(virtual_addresses, pagefaults, hits, misses)

if __name__ == '__main__':
    main()