import sys
import argparse
from TLB import TLB
from PageTable import PageTable

# usage: memSim <reference-sequence-file.txt> <FRAMES> <PRA>


def calculate_page_number(address, page_size):
    binary_representation = format(10, '08b')

def print_stats(translatedAddr, pagefault, hit, miss):
    print("Number of Translated Addresses = %d" % translatedAddr)
    print("Page Faults = %d" % pagefault)
    print("Page Fault Rate = %.3f" % (pagefault/translatedAddr))
    print("TLB Hits = %d" % hit)
    print("TLB Misses = %d" % miss)
    print("TLB Miss Rate = %.3f" % (miss/translatedAddr))

def main():
    parser = argparse.ArgumentParser(prog='MemSim', description='Simulate memory management')
    parser.add_argument('filename', help='Path to the input file')
    parser.add_argument('--frames', type=int, default=256, help='Number of frames in the system')
    parser.add_argument('--pra', choices=['FIFO', 'LRU', 'OPT'], default='FIFO', help='Page replacement algorithm')
    args = parser.parse_args()
    print_stats()

if __name__ == '__main__':
    main()