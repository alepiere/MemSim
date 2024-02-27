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
    print("Page Fault Rate = %.3f" % (pagefaults/len(translatedAddr)))
    print("TLB Hits = %d" % hits)
    print("TLB Misses = %d" % misses)
    print("TLB Miss Rate = %.3f" % (misses/len(translatedAddr)))

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
            frame_data = Memory.get_frame_data(frame_number)
            data_value = frame_data[page_offset:page_offset+1]
        else: 
            misses += 1
            frame_number = page_table.lookup(page_number)
            if frame_number is not None:
                # get frame from page table
                frame_data = Memory.get_frame_data(frame_number)
                data_value = frame_data[page_offset:page_offset+1]
            else:
                frame_data = pageFaultHandler(page_number)
                print(frame_data)
                print(page_number)
                memory.data[page_number] = frame_data
                data_value = frame_data[page_offset:page_offset+1]
                pagefaults += 1
                # go into back storage and get the page
        print(int.from_bytes(data_value))
        
    print_stats(virtual_addresses, pagefaults, hits, misses)

if __name__ == '__main__':
    main()