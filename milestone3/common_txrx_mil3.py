import numpy
import math as m
import operator

# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier 
  of frequency fc, sampled at samplerate
  '''
  print "MODULATE", fc, samplerate, len(samples)
  y = []
  fs = 1.0 / samplerate

  #carrier = cos(2 * math.pi * fc / fs * n)
  for n in range(0, len(samples)):
    y.append(samples[n] * m.cos(2 * m.pi * fc / fs * n))
  return y

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  
  return 0

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  
  # compute the demodulated samples
  return 0

