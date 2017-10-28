from ciphertools import *
from math import log, exp
from random import random
from string import replace
from itertools import product
import sys
global LW, RW, PROBS, ciphers, qw, LL, RL, allbigrams
letters ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
allbigrams = ["".join(i) for i in product(*[letters, letters])]

LW = [6, 5, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
LL = ['QR', 'TM', 'NL', 'DU', 'DM', 'WB', 'TQ', 'SE', 'RY', 'RQ', 'RC', 'NR', 'BQ', 'BD', 'YK', 'YE', 'XR', 'UF', 'TW', 'TV', 'TL', 'SQ', 'SF', 'SD', 'RL', 'RI', 'RH', 'RF', 'RE', 'RD', 'RB', 'RA', 'QK', 'QB', 'PO', 'PD', 'NQ', 'NK', 'ND', 'MY', 'MN', 'ME', 'MD', 'LK', 'LE', 'LC', 'HW', 'HP', 'HL', 'GM', 'EQ', 'EO', 'EL', 'EK', 'ED', 'EC', 'DV', 'DR', 'DL', 'DE', 'DC', 'CW', 'CP', 'CO', 'CD', 'CB', 'BY', 'BT', 'BO', 'BH', 'AL']

RW = [7, 4, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
RL = ['EH', 'NT', 'KN', 'TM', 'VH', 'UH', 'TY', 'OY', 'OT', 'LY', 'LE', 'FW', 'EP', 'EL', 'DN', 'BH', 'YT', 'YH', 'YD', 'WK', 'WE', 'VD', 'UW', 'UR', 'UE', 'TU', 'TN', 'ST', 'SK', 'SD', 'SB', 'RY', 'RV', 'RS', 'QV', 'QT', 'QS', 'QH', 'PT', 'PD', 'OW', 'OU', 'OS', 'OR', 'OM', 'OL', 'OC', 'NV', 'NH', 'MQ', 'MO', 'ML', 'MB', 'LU', 'LO', 'LN', 'LK', 'LF', 'LD', 'KM', 'HZ', 'HT', 'HK', 'FV', 'FL', 'EW', 'EN', 'EK', 'ED', 'CV', 'CH', 'BK']

ls = log(sum(map(exp, bw.values())))
PROBS = {}
for i in bw:
 PROBS[i] = exp(bw[i]-ls)

def runSample():
    ll = []; li = 0; ls = sum(LW)
    rl = []; ri = 0; rs = sum(RW)
    
    Q = 1
    
    while (li < len(LW) or ri < len(RW)):
        # take the bigger number at "head" of each list
        lk = LW[li] if li < len(LW) else -1
        rk = RW[ri] if ri < len(RW) else -1        
        
        k, l, s, W = lk, ll, ls, LW
        if lk <= rk:
            k, l, s, W = rk, rl, rs, RW
            ri += 1
        else:
            li += 1
        
        # run through possible replacements, calc prob of each
        poss = [b for b in PROBS if b not in l]
        tw = 0.
        current = ""
        currentp = 0.
        for b in poss:
            p = PROBS[b]
            w = p**k * (Q - p)**(sum(W[k+1:]))


            tw += w
            if tw * random() < w:
                current = b
                currentp = p
            # print b, w, tw, current
        l.append(current)
        Q -= p

    return ll, rl
    
def decrypt(ll, rl):
    out = []
    for c in ciphers:
        cc = c
        for pt,ct in zip(ll, LL):
            cc = replace(cc, " "+ct,  pt.lower())
        for pt,ct in zip(rl, RL):
            cc = replace(cc, ct+" ",   pt.lower())
        out.append( (cc, scoreText(cc, quadgrams=qw) ))
    score = sum([i[1] for i in out])
    return [i[0] for i in out], score

    
def hillClimb(ll, rl):
    base = decrypt(ll, rl)
    best = base[1], ll, rl
    b0 = best[0]
    # try swapping each element of ll in turn with every possible
    # bigram
    templl = [i for i in ll]
    temprl = [i for i in rl]
    for L, TL in [(ll, templl), (rl, temprl)]:
        for i in L:
            print "\b-",
            sys.stdout.flush()
            for j in allbigrams:
                try:
                    a, b = L.index(i), L.index(j)
                    TL[a], TL[b] = j, i
                except:
                    a = L.index(i)
                    b = None
                    TL[a] = j
                    nxt = decrypt(templl, temprl)
                if nxt[1] > best[0]:
                    best = nxt[1], [ii for ii in templl], [ii for ii in temprl]
                TL[a] = i
                if b is not None:
                    TL[b] = j
    print
    b= decrypt(best[1], best[2])
    print b[1]
    print "\n".join(b[0])
    print
    return best, best[0] > b0        
                
def go():
    ll, rl = runSample()
    while True:
        best, better = hillClimb(ll, rl)
        if not better:
            break
        s, ll, rl = best
    return decrypt(ll, rl)
    
best = (None, -1)
while True:         
    res = go()
    score = res[1]
    if score > best[1]:
        print "NEW RECORD:"
        best = res
        print "\n".join(best[0])
        print best[1]
