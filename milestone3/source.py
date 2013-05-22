# audiocom library: Source and sink functions
from common_srcsink import *
import Image
from graphs import *
import binascii
import random


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
                databits = list(sourcebits)
                header = self.get_header(SRCTYPE_MON, len(databits), None)
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
        while len(key) < SYMBOLSIZE:
            key = key + '0'
        return key

    def get_stats(self, data):
        # freq is a map of symbols to frequencies in this data
        freq = dict()
        for i in xrange(0, len(data), SYMBOLSIZE):
            key = key_from_arr(data[i:i+SYMBOLSIZE])
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
    # Returns map of frequencies for each symbol, as well as huffman-encoded bits
    def huffman_encode(self, sourcebits):
        print "huffman_encode sourcebits", key_from_arr(sourcebits)

        freq, stats = self.get_stats(sourcebits)
        mapping = huffman_lookup_table(stats)
        print "huffman_encode lookup table", mapping

        huffman_bits_str = ''
        for i in xrange(0, len(sourcebits), SYMBOLSIZE): # build the huffman-encoded bits
            key = key_from_arr(sourcebits[i:i+SYMBOLSIZE])
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

        payload_str = '{0:016b}'.format(payload_length)
        payload_arr = list(payload_str)
        payload_bits = [int(b) for b in list(payload_str)]

        if srctype == SRCTYPE_MON:
            header = srctype_bits + payload_bits
        else:
            stats_bits = []
            klist = []
            generate_keys(klist)
            for key in klist:
                if key in stats:
                    freq_str ='{0:010b}'.format(stats[key])
                else:
                    freq_str ='{0:010b}'.format(0)
                freq_bits = [int(b) for b in list(freq_str)]
                stats_bits = stats_bits + freq_bits
            header = srctype_bits + payload_bits + stats_bits

        return header
