import numpy
import math as m
import operator
import time

class Timer:    
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
# Methods common to both the transmitter and receiver
def modulate(fc, samplerate, samples):
  '''
  A modulator that multiplies samples with a local carrier 
  of frequency fc, sampled at samplerate
  '''
  #print "MODULATE", fc, samplerate, len(samples)
  try:
    with Timer() as t:
        y = []
        fs = samplerate
        omega_c = 2 * m.pi * fc / fs

        temp = range(0, len(samples))
        carrier = [m.cos(omega_c * n) for n in temp]
        y = numpy.multiply(samples, carrier)
  finally:
    print('Modulation took %.03f sec.' % t.interval)

  return y

def demodulate(fc, samplerate, samples):
  '''
  A demodulator that performs quadrature demodulation
  '''
  try:
    with Timer() as t:
      fs = samplerate
      omega_c = 2 * m.pi * fc / fs
      

      temp = range(0, len(samples))
      omega = [1j * omega_c * n for n in temp]
      carrier = [numpy.power(m.e, om) for om in omega]
      w = numpy.multiply(samples, carrier)

  finally:
    print('Demodulation took %.03f sec.' % t.interval)
  


  try:
    with Timer() as t:
      demod_samples = lpfilter(w, omega_c / 2.0)
  finally:
    print('LPF took %.03f sec.' % t.interval)
  
  return [numpy.linalg.norm(n) for n in demod_samples]

def lpfilter(samples_in, omega_cut):
  '''
  A low-pass filter of frequency omega_cut.
  '''
  # set the filter unit sample response
  L = 50
  h = []
  dmod = []

  h1range = range(-L, 0)
  h2range = range(1, L + 1)
  h1 = [m.sin(omega_cut * n) / (m.pi / n) for n in h1range]
  h2 = [m.sin(omega_cut * n) / (m.pi / n) for n in h2range]
  h = h1 + [omega_cut / m.pi] + h2

  #Demodulating samples
  for n in range(0, len(samples_in)):

    sl = 0 if n - L < 0 else n - L
    su = len(samples_in) - 1 if n + L > len(samples_in) - 1 else n + L + 1
    s_in = samples_in[sl:su]
    
    #hl = 0 if n - L >= 0 else - (n - L)
    #hu = len(h) if n + L <= len(samples_in) - 1 else len(h) + ((len(samples_in) - 1) -  (n + L + 1)) 
    #sum = 0
    #print sl, su, n, L
    addzerol = numpy.zeros(sl - (n - L))
    addzerou = numpy.zeros((n + L) - su + 1)

    #print addzerol, s_in, addzerou, len(addzerol), len(s_in), len(addzerou)
    s_in = numpy.concatenate((addzerol, s_in, addzerou)).flatten()
    dmod.append(numpy.dot(s_in, h))

    #print len(s_in), len(h)

    #h_in = h[hl:hu]
    #for i in range(0, len(h_in)):
     # sum += s_in[i] * h_in[i]
    #dmod.append(sum)

  return dmod
  

