import math
import common_txrx as common
import numpy
from common_txrx import *
from hamming_db import *

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence, cc_len):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence        
        self.preamblebits = [1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0]

        self.cc_len = cc_len
        self.headerencoding = 3
        self.cheaderlen = 18 * 3 # 16-bit coded length + 2-bit index value
        print 'Transmitter: '


    def encode(self, databits):
        # Encode the databits
        index, coded_databits = self.hamming_encoding(databits, False)

        # Compute length of the coded header + coded databits for use in the outer header
        coded_length = self.cheaderlen + len(coded_databits)
        
        # Create the outer header bits
        headerbits = int_to_bits(coded_length, 16) + int_to_bits(index, 2)

        # Encode the outer header 
        hindex, coded_header = self.hamming_encoding(headerbits, True)

        # Combine the coded outer header with coded databits
        coded_bits = coded_header + coded_databits
        return coded_bits

    def hamming_encoding(self, databits, is_header):
        if (is_header):
            encodingval = self.headerencoding
        else:
            encodingval = self.cc_len
        n, k, index, G = gen_lookup(encodingval)

        print n, k, index, G

        while len(databits) % k != 0:
            databits.append(0)

        coded_bits = []
        for i in range(len(databits) / k):
            d = databits[i:i + k]
            if (k == 1):
                c = d[0] * G
            else:
                c = numpy.dot(d, G)
            coded_bits = coded_bits + list(c)

        print databits
        print coded_bits

        return index, coded_bits

    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''
        # fill in your implementation
        silencebits = numpy.zeros(self.silence)
        databits_with_preamble = numpy.array(map(int, numpy.concatenate([silencebits, self.preamblebits, databits])))
        return databits_with_preamble


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        # fill in your implemenation
        samples = []
        for s in databits_with_preamble:
            if not s:
                samples.append(numpy.zeros(self.spb))
            else:
                samples.append(self.one * numpy.ones(self.spb))
        samples = numpy.array(map(int, numpy.concatenate(samples)))
        return samples
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)
