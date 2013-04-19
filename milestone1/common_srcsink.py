import numpy
import math
import operator

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

    ber = hamming_d / len(s1)
    return hamming_d, ber
