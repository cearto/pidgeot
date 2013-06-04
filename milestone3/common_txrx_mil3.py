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
  fs = samplerate

  #carrier = cos(2 * math.pi * fc / fs * n)
  omega_c = 2 * m.pi * fc / fs
  for n in range(0, len(samples)):
    y.append(samples[n] * m.cos(omega_c * n))
  return y

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  fs = samplerate
  omega_c = 2 * m.pi * fc / fs
  w = []

  for n in range(0, len(samples)):
    w.append(samples[n] * m.e^(1j * omega_c * n))

  lpfilter(w, omega_c / 2.0)
  return 0

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  h = []
  for n in range(-L , L)
    if n == 0:
      h.append(omega_cut / pi)
    else:
      h.append( m.sin(omega_cut * n) / m.pi / n
  
  # compute the demodulated samples
  demod_samples = []
  for n in range(0, len(samples_in))
    demod_samples[n] = samples_in[n] * m.e(1j * omega_cut * n) * h[n]
  return demod_samples

