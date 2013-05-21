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
        print 'Source: '

    def process(self):
            # Form the databits, from the filename 
            if self.fname is not None:
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    sourcebits = self.bits_from_image(self.fname)
                    databits = self.huffman_encode(sourcebits)
                    header = self.get_header(len(sourcebits), SRCTYPE_IMG)
                    print '\tSource type:\timage'
                    print '\tPayload length:\t', len(sourcebits)
                    print '\tHeader:\t', list(header)
                    # It's an image
                else:           
                    sourcebits = self.text2bits(self.fname)
                    databits = self.huffman_encode(sourcebits)
                    header = self.get_header(len(sourcebits), SRCTYPE_TXT)
                    print '\tSource type:\ttext'
                    print '\tPayload length:\t', len(sourcebits)
                    print '\tHeader:\t', list(header)
                    # Assume it's text                    
            else:        
                sourcebits = numpy.ones(self.monotone, dtype=numpy.int)
                databits = self.huffman_encode(sourcebits)
                header = self.get_header(len(sourcebits), SRCTYPE_MON)
                print '\tSource type: monotone'  
                print '\tPayload length:\t', len(sourcebits)   
                print '\tHeader:\t', list(header)
                # Send monotone (the payload is all 1s for 
                # monotone bits)
            databits = numpy.concatenate([header, databits])
            return sourcebits, databits
            # payload is the binary array of the file, databits is header + payload

    def get_stats(self, data):
        symbolsize = 4 

        # freq is a map of symbols to frequencies in this data
        freq = dict()
        for i in xrange(0,len(data),symbolsize):
            key = numpy.array_str(data[i:i+symbolsize])
            key = key.replace('[', '')
            key = key.replace(']', '')
            key = key.replace(' ', '')
            if key not in freq:
                freq[key] = 0
            else:
                freq[key] = freq[key] + 1

        # stats is an array of [freq, symbol] tuples to allow for heapify
        stats = []
        for key in freq:
            tp = [freq[key], key]
            stats.append(tp)
        return stats

    # This method borrows code from: http://en.literateprograms.org/Huffman_coding_(Python)
    def huffman_encode(self, sourcebits):
        stats = self.get_stats(sourcebits)
        htree = heapq.heapify(stats)
        while len(htree) > 1:
            left, right = heapq.heappop(htree), heapq.heappop(htree)
            parent = (left[0] + right[0], left, right)
            heapq.heappush(htree, parent)
        print htree


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

    def get_header(self, payload_length, srctype):
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        
        payload_str = '{0:032b}'.format(payload_length)
        payload_arr = list(payload_str)
        payload_bits = numpy.array(map(int, payload_arr))

        srctype_str = '{0:02b}'.format(srctype)
        srctype_arr = list(srctype_str)
        srctype_bits = numpy.array(map(int, srctype_arr))

        header = numpy.concatenate([srctype_bits, payload_bits])

        return header
