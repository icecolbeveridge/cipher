from itertools import permutations
from math import exp, factorial, log
from logfact import *
from random import random, choice, shuffle

CIPHERTEXT = "DUTMUFVDBHWKRHENRDOYLCVHNRLDQBORTMKNTVDNTMYHTQSBECUHLEMLRFLKDMNHYEOYCOMBNLQSTMKNCDKMNLOCRQBHRCNVHPLEDMNTTWFLRELYQREHSDLNBQEWEDLOQREHDUDNNQOWQREHDCNT  DUTMCBFVRQBHMEOTNKMQNDMOSFWEHLEKRCUWQREHDMNTRBUEEKRSQREHCWRVEQTYSEPDMNLEELLUTMKNWBEPRISDGMOSRLEL  EOCHTQOLBTOUQREHDVTMNRLFDUTNDRSKMYHTDMNTQKYDBYCVPDURBOHKRYELTLOTBDVHBQRYRYBKPOFWDELYSEPTLKOMTMKNKREHHWTYNLAZCPQVBDUH"

LETTERS = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

COUNTS = {}
for i in LETTERS:
    COUNTS[i] = CIPHERTEXT.count(i)

probs = {   "A": 0.082, "N": 0.067 ,
            "B": 0.015, "O": 0.075,
            "C": 0.028, "P": 0.019,
            "D": 0.043, "Q": 0.001,
            "E": 0.127, "R": 0.060,
            "F": 0.022, "S": 0.063,
            "G": 0.020, "T": 0.091,
            "H": 0.061, "U": 0.028,            
            "I": 0.072, "V": 0.010,
                        "W": 0.024,
            "K": 0.008, "X": 0.002,
            "L": 0.040, "Y": 0.020,
            "M": 0.024, "Z": 0.001 } 

def logpoisson( x, l ):
    return -l + x*log(l) - logfact(x)

def calcProb( row ):
    # what is the likelihood of this set of five characters forming a row, given the output
    lp = 0.
    for i in range(5):
        c = COUNTS[row[i]]
        l = 0.
        for j in [1,2,3,4,4]:
            jj = (i+j) % 5
            l += probs[row[jj]]
        l *= 0.2*len(CIPHERTEXT)    
        lp += logpoisson(c, l)
    return lp

def decrypt( pairs, square ):
    # square is a dictionary that maps letters to coordinates and vice-versa
    out = ""
    for p in pairs:
        fi, fj = square[p[0]]
        si, sj = square[p[1]]
        if fj == sj:
            # same row: bump both back one
            out += square[ ((fi + 4) % 5,fj)] + square[( (si + 4) % 5,sj)]
        elif fi == si:
            # same col: bump both up one
            out += square[ (fi,(fj + 4) % 5)] + square[ (si,(sj + 4) % 5)]
        else:
            out += square[ (fi,sj)] + square[(si,fj)]
    return out

def pickRandomRow( lst, avoid = "", addwt = 0. ):
    out = (-1e30, None)
    for weight, value in lst:
        # sod it
        r = random() ** (1./exp(weight+addwt))
        if len(set(value) & set(avoid)) != 0:
            r = -1e40
        if out[0] < r: 
            out = r, value
            #print r, value, weight+addwt
    return out[1]

def cycle( s ):
    i = choice ( range (len(s) ) )
    return s[i:] + s[:i]
        
def reservoirLogs( rowLogProbs ):
    # pick five non-intersecting rows from the table, weighted by probability
    avoid = ""
    sq = []
    for i in range(5):
        nxt = pickRandomRow(rowLogProbs, avoid = avoid, addwt=20.)
        avoid += (nxt)
        sq.append(cycle(nxt))
    # now make it a good square
    shuffle( sq )
    
    out = {}
    
    for i in range(5):
        for j in range(5):
            out[(i,j)] = sq[i][j]
            out[sq[i][j]] = (i,j)
    return out
  
def splitInPairs(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
  
rlp = []
for first in LETTERS[:-5]:
    best = (None,None)
    s = LETTERS.split(first)[1]
    for tail in permutations(s, 4):
        row = first + "".join(tail)
        lp = (calcProb(row), row)
        rlp.append(lp)
        if best[0] is None or best < lp:
            best = lp
    print best

print 

print "rows computed"
pairs = splitInPairs(CIPHERTEXT)
pairs = [p for p in pairs if p != "  "]
for i in range(100):
    sq = reservoirLogs( rlp )
    for i in range(5):
        for j in range(5):
            print sq[(i,j)],
        print
    print decrypt( pairs, sq )
        