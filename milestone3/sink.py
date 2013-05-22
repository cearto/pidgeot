# audiocom library: Source and sink functions
from common_srcsink import *
import Image
from graphs import *
import binascii
import random
import os
import heapq # for huffman tree


class Sink:
    def __init__(self): 
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        # Return the received payload for comparison purposes
        [srctype, payload_length] = self.read_type_size(recd_bits[:HEADER_GEN_LEN])
        if srctype != SRCTYPE_MON:
            stats = self.read_stat(recd_bits[HEADER_GEN_LEN:HEADER_GEN_LEN + HEADER_STATS_LEN])
            rcd_payload = self.huffman_decode(stats, recd_bits[HEADER_GEN_LEN + HEADER_STATS_LEN:HEADER_GEN_LEN + HEADER_STATS_LEN + payload_length])
        else:
            rcd_payload = recd_bits[HEADER_LEN:HEADER_LEN + payload_length]
        print '\tRecd ', len(recd_bits) - HEADER_LEN, ' data bits:'

        if srctype == SRCTYPE_TXT:
            print '\tText recd: ', self.bits2text(rcd_payload)
        elif srctype == SRCTYPE_IMG:
            self.image_from_bits(rcd_payload, "rcd-image.png")
        return rcd_payload

    def huffman_decode(self, stats, bits):
        print "len of undecoded bits", len(bits)
        mapping = huffman_reverse_lookup_table(stats)
        print "huffman_decode lookup table", mapping
        decoded_str = ''
        i = 0
        while i < len(bits):
            key = str(bits[i])
            i = i + 1
            while key not in mapping:
                key = key + str(bits[i])
                i = i + 1
            decoded_str = decoded_str + mapping[key]
        print decoded_str, len(decoded_str), len(decoded_str)/SYMBOLSIZE
        return bits

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        #array to binary string
        text = ''.join(str(e) for e in bits) 
        #binary to hex
        text = "%x" % int(text, 2)
        #hex to ascii
        text = binascii.unhexlify(text)

        return text

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .
        data = ''.join(str(e) for e in bits)
        data = "%x" % int(data, 2)

        imgSize = (32, 32)
        data = binascii.unhexlify(data)

        img = Image.fromstring('L', imgSize, data)
        img.save(filename)

        pass 

    def read_stat(self, ext_header):
        stats = []
        klist = []
        generate_keys(klist)
        for i in xrange(0, len(ext_header), STATSIZE):
            freq_bits = ext_header[i:i+STATSIZE]
            freq_str = key_from_arr(numpy.array(freq_bits))
            freq = int(freq_str, 2)
            if freq > 0:
                tp = (freq, klist[i/STATSIZE])
                stats.append(tp)
        print stats
        return stats

    def read_type_size(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        src_str = ''.join(map(str, header_bits[0:2]))
        src_int = int(src_str, 2)

        if src_int == SRCTYPE_MON:
            srctype = SRCTYPE_MON
            srctypestr = 'monotone'
        elif src_int == 1:
            srctype = SRCTYPE_IMG
            srctypestr = 'image'
        elif src_int == 2:
            srctype = SRCTYPE_TXT
            srctypestr = 'text'
        else: 
            print "INVALID SRCTYPE"

        payload_str = ''.join(map(str, header_bits[3:34]))
        payload_length = int(payload_str, 2)

        print '\tRecd header: ', header_bits
        print '\tSource type: ', srctypestr
        print '\tLength from header: ', payload_length

        return srctype, payload_length
