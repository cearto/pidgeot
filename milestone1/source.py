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
                    payload = bits_from_image(self, self.fname)
                    # Its an image
                else:           
                    payload = text2bits(self, self.fname)
                    # Assume it's text                    
            else:               
                payload = numpy.ones(self.monotone, dtype=numpy.int)
                header = self.get_header(len(payload), SRCTYPE_MON)
                databits = numpy.concatenate([header, payload])
                print "payload"
                print payload
                print "databits"
                print databits
                # Send monotone (the payload is all 1s for 
                # monotone bits)   
            return payload, databits
            # payload is the binary array of the file, databits is header + payload

    def text2bits(self, filename):
        f = open(filename)
        print f
        # Given a text file, convert to bits
        return bits

    def bits_from_image(self, filename):
        # Given an image, convert to bits
        return bits

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
