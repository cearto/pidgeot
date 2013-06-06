import numpy
import math
import operator
import common_txrx_mil3
import binascii
# Methods common to both the transmitter and receiver

'''
These functions are for modulation and demodulation
(which is currently presented as a black box)
No need to touch them
'''
def modulate (fc, samplerate, samples):
   return common_txrx_mil3.modulate(fc, samplerate, samples) 

def demodulate (fc, samplerate, samples):
   return common_txrx_mil3.demodulate(fc, samplerate, samples)

################
'''
If you need any functions that 
you need commonly in both transmitter and receiver,
implement here
'''

def int_to_bits (i, length):
	bits = list('{0:02b}'.format(i))
	bits = [int(b) for b in bits]
	while len(bits) < length:
		bits.insert(0, 0)
	return bits

def bits_to_int (bits):
	val = 0
	for i in range(len(bits)):
		if bits[i] == 1:
			addval = 2 ** (len(bits) - 1 - i)
			val = val + addval
	return val