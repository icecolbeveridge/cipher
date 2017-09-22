# crypto 
from numpy import *
from random import shuffle
from itertools import product
global LETTERS
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BIGRAMS = ["%s%s" % (i[0],i[1]) for i in product(LETTERS, repeat = 2)]
def bigramToNumber(big):
    i = LETTERS.find(big[0])*26
    j = LETTERS.find(big[1])
    return i+j

def numberToBigram(num):
    j = LETTERS[num//26]
    i = LETTERS[num % 26]
    return j+i
    
def generateTransitionMatrix():
    f = open("english_quadgrams.txt",'r')
    d = {}
    di = {}
    tot = 0.
    for l in f.readlines():
        q, n = l.split(" ")
        q1 = q[:2]
        q2 = q[2:]
        n = float(n)
        tot += n
        d[(q1,q2)] = n
        di[(q2,q1)] = n
    m = zeros((676,676), dtype=float)
    mi = zeros((676,676), dtype=float) 
    for i in d:
        n1 = bigramToNumber(i[0])
        n2 = bigramToNumber(i[1])
        m[n1,n2] = d[i] / tot
        mi[n2,n1] = d[i] / tot
    #m = stoch(m)
    #mi = stoch(mi)
    return m, mi
    
def getCipherTextPairs(ct):
    pairs = []
    for i in range(0, len(ct)-3, 2):
        p1 = bigramToNumber(ct[i:i+2])
        p2 = bigramToNumber(ct[i+2:i+4])
        pairs.append((p1, p2))
    return pairs
    
def generateInitialProbMatrix(pairs):
    return ones((676,676), float) / 676. # can make this more sophistimicated in time
    
def stoch(m, n=30):
    M = m.copy()
    for i in range(n):
        M = M/M.sum(axis=0)[None,:]
        M = M/M.sum(axis=1)[:,None]
    return M
   
def printBigramScores(big, mn = 0.01):
    j = bigramToNumber(big)
    for k in range(676):
        if P[k,j] > mn:
            print big, numberToBigram(k), P[k,j]

    

CIPHERTEXT = "DUTMUFVDBHWKRHENRDOYLCVHNRLDQBORTMKNTVDNTMYHTQSBECUHLEMLRFLKDMNHYEOYCOMBNLQSTMKNCDKMNLOCRQBHRCNVHPLEDMNTTWFLRELYQREHSDLNBQEWEDLOQREHDUDNNQOWQREHDCNT","DUTMCBFVRQBHMEOTNKMQNDMOSFWEHLEKRCUWQREHDMNTRBUEEKRSQREHCWRVEQTYSEPDMNLEELLUTMKNWBEPRISDGMOSRLEL","EOCHTQOLBTOUQREHDVTMNRLFDUTNDRSKMYHTDMNTQKYDBYCVPDURBOHKRYELTLOTBDVHBQRYRYBKPOFWDELYSEPTLKOMTMKNKREHHWTYNLAZCPQVBDUH"

LAMBDA = 0.8
T, TI = generateTransitionMatrix()

pairs = getCipherTextPairs(CIPHERTEXT[0]) # eg (453, 521)

P = generateInitialProbMatrix(pairs)
P = stoch(P, n=100)

for i in range(2000):
    print i
    shuffle( pairs )
    for p in pairs:
        p1 = transpose(P[:,p[0]])
        p2 = transpose(P[:,p[1]])
        
        q1 = transpose(TI.dot(p2))
        q2 = transpose(T.dot(p1))
                
        q1 = q1/sum(q1)
        q2 = q2/sum(q2)

        
        P[:,p[0]] = LAMBDA * p1 + (1-LAMBDA) * q1
        P[:,p[1]] = LAMBDA * p2 + (1-LAMBDA) * q2
        
        if amin(P) < 0:
            print p1, p2, q1, q2
            raise ValueError
        
        P = stoch(P, n=1)
        
    for i in BIGRAMS:
        printBigramScores(i, 0.02)

