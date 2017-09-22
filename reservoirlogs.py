from random import random, choice
from collections import defaultdict
from math import log
from itertools import product

def getBigrams ( filename ):
    f = open(filename, 'r')
    out = []
    for l in f.readlines():
        big, weight = l.split(" ")
        out.append((big, float(weight)))
    return out

def getQuads( filename ):
    f = open(filename,'r')
    out = defaultdict( list )
    for l in f.readlines():
        word, weight = l.split(" ")
        out[ word[:2] ].append( (word[2:], float(weight)) )
    return out

def pickRandom( lst, avoid=[] ):
    # list of tuples, (value, weight)
    out = (0, None)
    for value, weight in lst:
        r = random() ** (1./weight)
        if value in avoid:
            r = 0.
        if out[0] < r:
            out = r, value
    return out[1]
    
def rev( s ):
    return s[::-1]
    
def splitInPairs(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
    
def scoreString( s, Q ):
    pairs = splitInPairs(s)
    tot = 0.
    for i in range(len(pairs)-1):
        p = pairs[i]
        q = pairs[i+1]
        try:
            w = [j[1] for j in Q[p] if j[0] == q][0]

        except IndexError:
            w = 1.e10    
        tot += log(w)            

    return tot
    
def getAvoid( big ):
    # for TU, avoid T? and ?U
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    av = ["".join(i) for i in product(big[0], LETTERS)]
    av.extend(["".join(i) for i in product(LETTERS, big[1])])
    return av
    
CIPHERTEXT = "DUTMUFVDBHWKRHENRDOYLCVHNRLDQBORTMKNTVDNTMYHTQSBECUHLEMLRFLKDMNHYEOYCOMBNLQSTMKNCDKMNLOCRQBHRCNVHPLEDMNTTWFLRELYQREHSDLNBQEWEDLOQREHDUDNNQOWQREHDCNT","DUTMCBFVRQBHMEOTNKMQNDMOSFWEHLEKRCUWQREHDMNTRBUEEKRSQREHCWRVEQTYSEPDMNLEELLUTMKNWBEPRISDGMOSRLEL","EOCHTQOLBTOUQREHDVTMNRLFDUTNDRSKMYHTDMNTQKYDBYCVPDURBOHKRYELTLOTBDVHBQRYRYBKPOFWDELYSEPTLKOMTMKNKREHHWTYNLAZCPQVBDUH"

best = -1.E20
Q = getQuads( "english_quadgrams.txt" )
B = getBigrams( "english_bigrams.txt")
while True:
    C = choice(CIPHERTEXT)
    pairs = splitInPairs(C)


    mapping = {}
    av = getAvoid( pairs[0] )
    current = pickRandom( B, av )
    string = current
    mapping[ pairs[0] ] = current
    mapping[ rev(pairs[0]) ] = rev(current)
    for i in range(0, len(pairs) - 1):
        p = pairs[i]
        q = pairs[i+1]
        if q in mapping:
            current = mapping[q]
        else:
            av = mapping.values()
            av.extend(getAvoid(q))
            current = pickRandom( Q[current], avoid = av )
            mapping[q] = current
            mapping[ rev(q) ] = rev(current)
        string += current
    s = scoreString(string, Q) / len(string)
    
    if s > best:
        best = s
        bstring = string
    if s > 6.1 or s == best:
        print string, s
        print bstring, best
        print
    