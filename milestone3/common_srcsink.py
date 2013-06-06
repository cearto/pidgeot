import numpy
import math
import operator
import heapq # huffman

SYMBOLSIZE = 4
STATSIZE = 10
SRCTYPE_MON = 0
SRCTYPE_IMG = 1
SRCTYPE_TXT = 2
HEADER_GEN_LEN = 20
HEADER_STATS_LEN = 160
PADDING_BITS = 2

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
    if len(s1) > len(s2):
    	s1 = s1[:len(s2)]
    else:
    	s2 = s2[:len(s1)]

    hamming_d = 0
    pairs = zip(s1, s2)

    for a,b in pairs:
    	if a != b:
    		hamming_d = hamming_d + 1

    ber = hamming_d / float(len(s1))
    return hamming_d, ber

# This method takes code from: http://en.literateprograms.org/Huffman_coding_(Python)
def build_htree(stats):
    htree = heapq.heapify(stats)
    while len(stats) > 1: # build the huffman tree
        left, right = heapq.heappop(stats), heapq.heappop(stats)
        parent = (left[0] + right[0], left, right)
        heapq.heappush(stats, parent)
    htree = stats[0]
    return htree

# This method takes code from: http://en.literateprograms.org/Huffman_coding_(Python)
def map_huffman_tree(htree, mapping, prefix = ''):
    if len(htree) == 2:
        mapping[htree[1]] = prefix
    else:
        map_huffman_tree(htree[1], mapping, prefix + '0')
        map_huffman_tree(htree[2], mapping, prefix + '1')

def huffman_lookup_table(stats):
    htree = build_htree(stats)
    mapping = dict()
    map_huffman_tree(htree, mapping)
    return mapping

def huffman_reverse_lookup_table(stats):
    mapping = huffman_lookup_table(stats)
    rmapping = dict()
    for key in mapping:
        rmapping[mapping[key]] = key
    return rmapping

def generate_keys(klist,key='',size=SYMBOLSIZE):
    if len(key) == size:
        klist.append(key)
    else:
        generate_keys(klist, key+'0')
        generate_keys(klist, key+'1')

def str_from_arr(arr):
    s = numpy.array_str(arr)
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace(' ', '')        
    return s

def key_from_arr(arr):
    key = numpy.array_str(arr)
    key = key.replace('[', '')
    key = key.replace(']', '')
    key = key.replace(' ', '')            
    while len(key) < SYMBOLSIZE:
        key = key + '0'
    return key