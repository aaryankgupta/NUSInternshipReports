import itertools
import math
import operator as op
import sys
from decimal import *
from numpy import exp
from functools import reduce
from scipy.special import gammaln
from scipy.special import comb
if sys.version_info[0] < 3:
    range = xrange

    filter = itertools.ifilter
    map = itertools.imap
    zip = itertools.izip

def memoize(f):
    """ Memoization decorator for a function taking one or more arguments. """
    class memodict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret

    return memodict().__getitem__

@memoize
def coomb(n, k):
    if (k > n) or (k < 0):
        return 0
    #return comb(n,k)
    return int(exp(Decimal(gammaln(n+1) - gammaln(n-k+1) - gammaln(k+1))))
# 
# 
# 
# 
#
#relevant code starts here
rho=1.1

#function which gives cominatorial term in summation for variance
@memoize
def computeterm(d, logsetsize, w):
    if(w>0):
        cterm= (w*w)*((4*math.e*math.sqrt(d*logsetsize)/w)**w)*(exp(logsetsize))
    else:
        cterm=coomb(d, w)
    return cterm


#function which gives value of sigma^2/E
@memoize
def computeratio(d, m, p,pivotfactor):
    sum = Decimal(0)
    sumval = 0
    n = min(d,m + pivotfactor)
    for w in range(n + 1):
        probcorr = math.log(1 + p**w)
        if m > 1:
            probcorr += reduce(op.add, (math.log(1 + p**w) for i in range(1, m)), 0)
        probcorr = exp(Decimal(probcorr)) - 1
        cterm = int(min(coomb(d, w), computeterm(d, n, w), (1 << n) - sumval))
        sumval += cterm
        term = cterm * Decimal(probcorr)
        sum += Decimal(term)+1
        if term == 0:
            break

    return round(sum / (1 << m), 2)




n = int(sys.argv[1])


#pivotfactor=l=log|S|
#Why is this taken to be constant? A roughMC call should have been made here.
pivotfactor = 9
thresh = 1.1

if (len(sys.argv) > 2):
     thresh = float(sys.argv[2])

for iteration in range(1,n+1):

    writeStr = []
    prev_max = 500
    prev_val = prev_max
    shouldexit = False
    prev_ratio = 0

    for i in range(1, iteration*100+1):
        decr = 15
        if (prev_val < 2/5*prev_max):
            decr = int(math.ceil(prev_val*1.0/40))
        density = 0.0
        for j in range(prev_val, 1, -decr):
            m = 1-(j*2.0/(2*prev_max))
            ratio = computeratio(iteration*100, i, m,pivotfactor)
            if (ratio > rho or (j < decr)):
                probval = (j+decr)*1.0/(2*prev_max)
                if (probval > 0.5):
                    probval = 0.5
                if (i < 10 and False):
                    probval = 0.5

                writeStr.append('%d/%d:%s' % (i,n, str(round(probval, 3))))
                print('%d/%d:%s' % (i,iteration*100,str(round(probval, 3))))
                density = probval
                prev_val = j+4*decr
                if (prev_val > prev_max):
                    prev_val = prev_max
                shouldexit = True
            prev_ratio = ratio
            if (shouldexit):
                shouldexit = False
                break
        if iteration*100*density < 40:
            break #stop if less than 40 1's in a row
    f = open('allvalues.txt', 'a')
    f.write('\n'.join(writeStr))
    f.write('\n')
    f.close()