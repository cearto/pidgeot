# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random

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
                    payload = self.bits_from_image(self.fname)
                    header = self.get_header(len(payload), SRCTYPE_IMG)
                    # Its an image
                else:           
                    payload = self.text2bits(self.fname)
                    header = self.get_header(len(payload), SRCTYPE_TXT)
                    print "Processing text:", self.fname
                    # Assume it's text                    
            else:               
                payload = numpy.ones(self.monotone, dtype=numpy.int)
                header = self.get_header(len(payload), SRCTYPE_MON)
                # Send monotone (the payload is all 1s for 
                # monotone bits)
            print 'SENDING ENCODING:', SRCTYPE_TXT, len(payload)
            print 'DATA: ', payload
            databits = numpy.concatenate([header, payload])
            return payload, databits
            # payload is the binary array of the file, databits is header + payload

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
