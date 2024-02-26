from TLB import TLB
from PageTable import PageTable



def parse_args

def print_stats(translatedAddr, pagefault, hit, miss):
    print("{}, {}, {}, {}".format(address, value, frame_num, frame_content))
    print("Number of Translated Addresses = %d" % translatedAddr)
    print("Page Faults = %d" % pagefault)
    print("Page Fault Rate = %.3f" % (pagefault/translatedAddr))
    print("TLB Hits = %d" % hit)
    print("TLB Misses = %d" % miss)
    print("TLB Miss Rate = %.3f" % (miss/translatedAddr))

def main():
    alg = ["FIFO", "LRU", "OPT"]

    print_stats

if __name__ == '__main__':
    main()