import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb 
        self.preamblebits = [1,1,1,1,1,0,1,1,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0]
        print 'Receiver: '

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
                samples.append(numpy.ones(self.spb)) # no self.one because it doesn't matter what you scale by
        samples = numpy.array(map(int, numpy.concatenate(samples)))
        return samples

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)
    def avg_middle_bits(self, bits):
        n = len(bits)
        center = n / 2
        offset = int(numpy.ceil(n / 4.0))
        if n % 2 == 0: 
            start = center - offset
        else: 
            start = center - offset + 1
        end = center + offset
        middle_bits = bits[start:end]
        avg = numpy.average(middle_bits)
        
        return avg

    def detect_energy_offset(self, demod_samples, thresh, one):
        windowsize = self.spb
        energy_offset = 0

        for i in range(0, len(demod_samples) - windowsize + 1):
            window = demod_samples[i: i + windowsize]
            if self.avg_middle_bits(window) > (one + thresh)/2.0:
                energy_offset = i
                break
        return energy_offset

    def detect_preamble_offset(self, demod_samples, energy_offset):
        preamble_samples = self.bits_to_samples(self.preamblebits)
        preamble_length = len(self.preamblebits) * self.spb
        endrange = min(len(demod_samples) - energy_offset - preamble_length + 1, energy_offset + 3 * preamble_length)
        cross_r = []
        
        for i in range(energy_offset, endrange):
            window = demod_samples[i: i + preamble_length]
            denom = numpy.linalg.norm(demod_samples[i: i + preamble_length])
            cross_r.append(numpy.dot(preamble_samples, window)/denom)

        value = max(cross_r)
        return cross_r.index(value)

    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''
        # Fill in your implementation of the high-energy check procedure

        energy_offset = self.detect_energy_offset(demod_samples, thresh, one) # fill in the result of the high-energy check
        if energy_offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''
        # Fill in your implementation of the cross-correlation check procedure
        
        preamble_offset = self.detect_preamble_offset(demod_samples, energy_offset)# fill in the result of the cross-correlation check 
        
        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''

        return energy_offset + preamble_offset
        
    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''
        npreamblebits = len(self.preamblebits) # number of bits in the preamble
        preamble_candidates = demod_samples[preamble_start : preamble_start + npreamblebits * self.spb]
        ones = []
        zeros = []
        avgs = []
        for i in range(0, npreamblebits):
            bit = preamble_candidates[i * self.spb : i * self.spb + self.spb] # all the samples in this bit
            avg = self.avg_middle_bits(bit)
            avgs.append(avg)
            if self.preamblebits[i]: # assign the sample to a zero or one bit
                ones.append(self.avg_middle_bits(bit))
            else:
                zeros.append(self.avg_middle_bits(bit))
        threshold = numpy.mean([numpy.mean(ones), numpy.mean(zeros)]) # calculate new threshold

        preamble_trans = []
        for i in avgs:
            if i > threshold:
                preamble_trans.append(1)
            else:
                preamble_trans.append(0)
                
        #print preamble_trans
        #print self.preamblebits

        recv_data_samples = demod_samples[preamble_start + npreamblebits * self.spb : -1]
        recv_data_bits = []
        # Fill in your implementation
        for i in xrange(0, len(recv_data_samples), self.spb):
            bit = recv_data_samples[i : i + self.spb]
            avg = self.avg_middle_bits(bit)
            if avg > threshold:
                recv_data_bits.append(1)
            else:
                recv_data_bits.append(0)
        #print recv_data_bits
        return recv_data_bits
        
    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
