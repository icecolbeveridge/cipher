from ciphertools import *
from math import log, exp
from random import random
from string import replace
global LW, RW, PROBS, ciphers, qw
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
def go():
    ll, rl = runSample()
    out = []
    for c in ciphers:
        cc = c
        for pt,ct in zip(ll, LL):
            cc = replace(cc, " "+ct,  pt.lower())
        for pt,ct in zip(rl, RL):
            cc = replace(cc, ct+" ",   pt.lower())
        out.append( (cc, scoreText(cc, quadgrams=qw) ))
    return out
    
best = (None, -1)
while True:         
    res = go()
    score = sum([i[1] for i in res])
    if score > best[1]:
        best = ( [i[0] for i in res], score)
        for b in best[0]:
            print b
        print best[1]
