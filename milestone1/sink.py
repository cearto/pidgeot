# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
import os

SRCTYPE_MON = 0
SRCTYPE_IMG = 1
SRCTYPE_TXT = 2
HEADER_LEN = 34

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
        [srctype, payload_length] = self.read_header(recd_bits[:HEADER_LEN])
        
        rcd_payload = recd_bits[HEADER_LEN:HEADER_LEN + payload_length]
        if srctype == SRCTYPE_TXT:
            print '\tText recd: ', self.bits2text(rcd_payload)
        elif srctype == SRCTYPE_IMG:
            self.image_from_bits(rcd_payload, "rcd-image.png")
        return rcd_payload

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
        print data

        img = Image.fromstring('L', imgSize, data)
        img.save(filename)

        pass 

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        src_str = ''.join(map(str, header_bits[0:2].tolist()))
        src_int = int(src_str, 2)

        if src_int == 0:
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

        payload_str = ''.join(map(str, header_bits[3:34].tolist()))
        payload_length = int(payload_str, 2)

        print '\tRecd header: ', header_bits
        print '\tSource type: ', srctypestr
        print '\tLength from header: ', payload_length
        
        return srctype, payload_length
