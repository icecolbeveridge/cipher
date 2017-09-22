# bijection between f1: c<->p, (. alpha alpha) <-> (alpha alpha)
# bijection between f2: c<->p, (alpha alpha .) <-> (alpha alpha)

# initially: each p_i = f(c_i) equally likely
# generate and score N ciphertexts
# if there's a new best, store it
# recalibrate probabilities (how?)
# repeat

# calibration plan:
# initially, each digraph has Index 0.
# Likelihood is proportional to some sigmoid function (1 / (1+e^(-S)))
# Use reservoir sampling to pick a pt digraph for each ct digraph
# Score pt based on quadgrams
# Update mean, variance
# Adjust Indexes for picked digraphs by (multiple of) z-score.
from random import random, choice
from math import exp
from ciphertools import *
from time import gmtime, strftime
N = 100
def sig(x):
    if x < 0:
        return exp(x) / (1. + exp(x))
    else:
        return 1. / (1. + exp(-x))

def drawSample(bij):
  out = {}
  k = bij.keys()
  while k:
    ki = choice(k)
    b = bij[ki] # plaintext pairs and indices
    poss = [i for i in b if i not in out.values()]
    # reservoir sample
    out[ki] = ""
    t = 0.
    for p in poss:
        t += sig(b[p])
        pr = sig(b[p])/t
        if random() < pr:
            out[ki] = p
    k.remove(ki)
  return out

b1 = {}
b2 = {}

for c in sc:
    for s in c:
      next = {}
      for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
          next[i+j] = 0.

      if s[0] == " ":
        b1[s] = next
      else:
        b2[s] = next
# b1 and b2 map front/back ciphertext pairs to plaintext pairs


while True:
    stats = []
    for i in range(N):
        s = drawSample(b1)
        s2 = drawSample(b2)
        s.update(s2)
        if i < 10:
            print s[" DU"], b1[" DU"][s[" DU"]]
        p = sum([scoreMapping(l, s, bw, qw) for l in links])
        stats.append((p, s))
    stats.sort()
    for i in range(N):
        adj =  ((N-i-1.)/(N-1.) - 0.5)* N**(-0.5)

        s = stats[i][1]
        for k in s:
            if k in b1:
                b1[k][s[k]] += adj
            if k in b2:
                b2[k][s[k]] += adj
    print
    print strftime("%Y-%m-%d %H:%M:%S", gmtime()), stats[0][0]
    print stats[-1][0]

    sss = [(b1[" DU"][k],k) for k in b1[" DU"]]
    sss.sort()
    print sss[-5:]
    print sss[:5]
        #print b1[" DU"]
    for c in sc:

        print translation(c, stats[0][1])
