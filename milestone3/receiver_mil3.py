import numpy
import math
import operator
import random
import scipy.cluster.vq
import common_txrx as common

def detect_threshold(demod_samples): 
        # Now, we have a bunch of values that, for on-off keying, are
        # either near amplitude 0 or near a positive amplitude
        # (corresp. to bit "1").  Because we don't know the balance of
        # zeroes and ones in the input, we use 2-means clustering to
        # determine the "1" and "0" clusters.  In practice, some
        # systems use a random scrambler to XOR the input to balance
        # the zeroes and ones. We have decided to avoid that degree of
        # complexity in audiocom (for the time being, anyway).

	# initialization
  centers = [min(demod_samples), max(demod_samples)]
  new_centers = centers #different to start k-means
  start = True
  # 2-means clustering   
  
  while new_centers != centers or start:
    start = False
    centers = new_centers
    # Assign each sample to its closest center
    Ck = [[], []]
    n = 0
    for s in demod_samples:
      diff = []
      for c in centers:
        diff.append(numpy.power(numpy.abs(s - c), 2))
      k = numpy.argmin(diff)
      Ck[k].append(n)
      n += 1
    # Recompute centers
    center_index = 0

    for center_set in Ck:
      sum = 0
      for n in center_set:
        sum += demod_samples[n]
      sum *= 1.0 / len(center_set)
      
      new_centers[center_index] = sum
      center_index += 1
 
  # associate the higher of the two centers 
  # with one and the lower with zero
  
  zero = min(centers)
  one = max(centers)

  #compute thresh
  thresh = (one + zero) / 2
  print "Threshold for 1:"
  print one
  print " Threshold for 0:"
  print zero
  print " Threshold"
  print thresh

  return one, zero, thresh

#detect_threshold([1,2,3, 30, 40, 50])
