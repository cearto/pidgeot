# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random
import heapq # for huffman tree

SRCTYPE_MON = 0
SRCTYPE_IMG = 1
SRCTYPE_TXT = 2

class Source:

    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        self.symbolsize = 4
        print 'Source: '

    def process(self):
            # Form the databits, from the filename 
            if self.fname is not None:
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    sourcebits = self.bits_from_image(self.fname)
                    stats, databits = self.huffman_encode(sourcebits)
                    header = self.get_header(SRCTYPE_IMG, len(databits), stats)
                    print '\tSource type:\timage'
                    print '\tPayload length:\t', len(databits)
                    print '\tHeader:\t', header
                    # It's an image
                else:           
                    sourcebits = self.text2bits(self.fname)
                    stats, databits = self.huffman_encode(sourcebits)
                    header = self.get_header(SRCTYPE_TXT, len(databits), stats)
                    print '\tSource type:\ttext'
                    print '\tPayload length:\t', len(databits)
                    print '\tHeader:\t', header
                    # Assume it's text                    
            else:        
                sourcebits = numpy.ones(self.monotone, dtype=numpy.int)
                stats, databits = self.huffman_encode(sourcebits)
                header = self.get_header(SRCTYPE_MON, len(databits), stats)
                print '\tSource type: monotone'  
                print '\tPayload length:\t', len(databits)   
                print '\tHeader:\t', header
                # Send monotone (the payload is all 1s for 
                # monotone bits)
            databits = header + databits
            return sourcebits, databits
            # sourcebits is the un-encoded array of bits of the file
            # databits is the header + encoded payload

    def key_from_arr(self, arr):
        key = numpy.array_str(arr)
        key = key.replace('[', '')
        key = key.replace(']', '')
        key = key.replace(' ', '')            
        while len(key) < self.symbolsize:
            key = key + '0'
        return key

    def get_stats(self, data):
        # freq is a map of symbols to frequencies in this data
        freq = dict()
        for i in xrange(0, len(data), self.symbolsize):
            key = self.key_from_arr(data[i:i+self.symbolsize])
            if key not in freq:
                freq[key] = 1
            else:
                freq[key] = freq[key] + 1

        # stats is an array of [freq, symbol] tuples to allow for heapify
        stats = []
        for key in freq:
            tp = (freq[key], key)
            stats.append(tp)
        return freq, stats

    # This method takes code from: http://en.literateprograms.org/Huffman_coding_(Python)
    def map_huffman_tree(self, htree, mapping, prefix = ''):
        if len(htree) == 2:
            mapping[htree[1]] = prefix
        else:
            self.map_huffman_tree(htree[1], mapping, prefix + '0')
            self.map_huffman_tree(htree[2], mapping, prefix + '1')

    # This method takes code from: http://en.literateprograms.org/Huffman_coding_(Python)
    # Returns map of frequencies for each symbol, as well as huffman-encoded bits
    def huffman_encode(self, sourcebits):
        freq, stats = self.get_stats(sourcebits)
        htree = heapq.heapify(stats)
        while len(stats) > 1: # build the huffman tree
            left, right = heapq.heappop(stats), heapq.heappop(stats)
            parent = (left[0] + right[0], left, right)
            heapq.heappush(stats, parent)
        htree = stats[0]
        mapping = dict() 
        self.map_huffman_tree(htree, mapping) # creates the lookup table

        huffman_bits_str = ''
        for i in xrange(0, len(sourcebits), self.symbolsize): # build the huffman-encoded bits
            key = self.key_from_arr(sourcebits[i:i+self.symbolsize])
            huffman_bits_str = huffman_bits_str + mapping[key]

        huffman_bits = list(huffman_bits_str)
        huffman_bits = [int(b) for b in huffman_bits]

        # Return frequency map and huffman-encoded bits
        return freq, huffman_bits

    def text2bits(self, filename):
        # Given a text file, convert to bits
        f = open(filename)
        text_str = f.read()
        f.close()
        text_bin = bin(int(binascii.hexlify(text_str), 16))
        text_arr = list(text_bin[2:]) # To get rid of the 0b prefix
        text_bits = numpy.array(map(int, text_arr))
        return text_bits 

    def bits_from_image(self, filename):
        # Given an image, convert to bits
        img = Image.open(filename).convert('L')
        img_arr = list(img.getdata())
        img_str = ''
        for p in img_arr:
            img_str += '{0:08b}'.format(p)
        img_bits = numpy.array(map(int, list(img_str)))
        return img_bits

    def get_header(self, srctype, payload_length, stats):
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        
        srctype_str = '{0:02b}'.format(srctype)
        srctype_arr = list(srctype_str)
        srctype_bits = [int(b) for b in list(srctype_str)]

        payload_str = '{0:032b}'.format(payload_length)
        payload_arr = list(payload_str)
        payload_bits = [int(b) for b in list(payload_str)]

        stats_bits = []
        for key in stats:
            key_bits = [int(b) for b in list(key)]
            freq_str ='{0:010b}'.format(stats[key])
            freq_bits = [int(b) for b in list(freq_str)]
            stats_bits = stats_bits + key_bits + freq_bits

        header = srctype_bits + payload_bits + stats_bits
        return header
