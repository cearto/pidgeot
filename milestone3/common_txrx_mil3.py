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
    w.append(samples[n] * numpy.power(m.e, 1j * omega_c * n))

  demod_samples = lpfilter(w, omega_c / 2.0)


  return [numpy.linalg.norm(n) for n in demod_samples]

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  h = []
  dmod = []

  for n in range(-L, L + 1):
    if n == 0:
      h.append(omega_cut / m.pi)
    else:
      h.append( m.sin(omega_cut * n) / (m.pi / n))
   

  #Demodulating samples
  for n in range(0, len(samples_in)):
    sl = 0 if n - L < 0 else n - L
    su = len(samples_in) - 1 if n + L > len(samples_in) - 1 else n + L + 1
    hl = 0 if n - L >= 0 else - (n - L)
    hu = len(h) if n + L <= len(samples_in) - 1 else len(h) + ((len(samples_in) - 1) -  (n + L + 1)) 
    sum = 0
    if not (hl == 0 and hu == 101):
    #  print sl, su, len(samples_in[sl: su])
    # print hl, hu, len(h[hl:hu])
    
    s_in = samples_in[sl:su]
    h_in = h[hl:hu]
    #print len(s_in), len(h_in)
    for i in range(0, len(h_in)):
      sum += s_in[i] * h_in[i]
    dmod.append(sum)

  return dmod
  

