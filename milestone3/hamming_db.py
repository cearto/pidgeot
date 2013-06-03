import numpy
import math
import operator
import common_txrx_mil3
import binascii
import sys

generating_matrices = [numpy.array([1, 1, 1]),
                       numpy.array([1,    1,    0,    1,    0,    0,    0,
                                    0,    1,    1,    0,    1,    0,    0,
                                    1,    1,    1,    0,    0,    1,    0,
                                    1,    0,    1,    0,    0,    0,    1]),
                       numpy.array([1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                    0,     1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                    0,     0,     1,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,
                                    1,     1,     0,     1,     0,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,
                                    1,     0,     1,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,     0,     0,
                                    0,     1,     0,     1,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,     0,
                                    1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,     0,     0,
                                    0,     1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,     0,
                                    1,     1,     1,     1,     0,     0,     0,     0,     0,     0,     0,     0,     1,     0,     0,
                                    1,     0,     1,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1,     0,
                                    1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     1]),
                       numpy.array([ 1,    0,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                     0,    1,    0,    1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
                                     0,    0,    1,    0,     1,     0,     0,     1,     0,     0,     0,     0,     0,     0,     0,     0,     0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    1,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    0,    1,    1,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    0,    0,    1,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     0,    0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    0,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,
                                     1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,
                                     0,    1,    1,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,    0,
                                     1,    0,    0,    1,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,    0,
                                     1,    1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,    0,
                                     1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,    0,
                                     0,    1,    1,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,    0,
                                     1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,
                                     0,    1,    0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1])]

parameters = [[3,1],[7,4],[15,11],[31,26]]

def rearrange_list(L, k, n):
    R = []
    for i in range(k):
        start = i * n
        row = L[start:start + n]
        sectionA = row[:n - k]
        sectionI = row[n - k:]
        row = list(sectionI) + list(sectionA)
        R = R + row
    return R

def gen_lookup(cc_len):
    ''' 
    returns
    (1) n (=cc_len, codeword length)
    (2) k (length of data bit in each codeword)
    (3) index (index of the corresponding code in the above lookup table)
    (4) generater matrix
    for Hamming code with n = cc_len
    '''
    if cc_len == 3:
        index = 0
    elif cc_len == 7:
        index = 1
    elif cc_len == 15:
        index = 2
    elif cc_len == 31:
        index = 3
    else:
        print '\tNo Hamming code with n =', cc_len
        sys.exit(1)

    n = parameters[index][0]
    k = parameters[index][1]
    
    # Reshape G:
    G = generating_matrices[index]
    G = rearrange_list(G, k, n)
    G = numpy.reshape(G, (k, n))
    return n, k, index, G

def parity_lookup(index):
    '''
    returns the
    (1) n (=cc_len, codeword length)
    (2) k (length of data bit in each codeword)
    (3) index (index of the corresponding code in the above lookup table)
    (4) parity check matrix
    matched by the lookup table above given the index
    The reason why this takes the index as the input while gen_lookup takes cc_len
    is, because containing index is efficient than containing n in the header.
    The decoder reads the header to pick the right parity check matrix.
    ''' 

    index = 1
    G = generating_matrices[index]
    n = parameters[index][0]
    k = parameters[index][1]
    
    # Reshape G, extract A and compute H:
    H = []
    I = numpy.identity(n - k, int)
    for r in range(n - k):
        row = []
        for c in range(k):
            val = G[c * n]
            row.append(val)
        Irow = I[r]
        for c in range(k, n):
            val = Irow[c - k]
            row.append(val)
        H.append(row)
    print H
    H = numpy.reshape(H, (n - k, n))

    return n, k, H



