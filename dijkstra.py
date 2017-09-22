# here's the plan
#
# Figure out score for each [bigram]->[bigram] and [start]->[bigram] using ngrams
# Read in ciphers
#
# Determine 'best path' through ciphers under constraints by generating odd and even mappings:
    # no plaintext pair can appear more than once in odd mapping or even mapping
from __future__ import print_function
import math, collections, operator, random, sys


def getScores( bigrams, quadgrams ):
    bout = {}
    qout = {}
    bf = open(bigrams, 'r')
    for r in bf.readlines()[1:]:
        print (r)
        b, s = r.split(",")
        bout[b] = math.log( float(s)+1 )
    bf.close()
    qf = open(quadgrams, 'r')
    for r in qf.readlines()[1:]:
        q, s = r.split(",")
        qout[ (q[:2], q[2:]) ] = math.log( float(s)+1 )
    return bout, qout

def splitCipher( ciph ):
    out = []
    while ciph:
        out.append( ciph[:3] )
        ciph = ciph[3:]

    return out

def createLinks( lst ):
    for i, e in enumerate(lst):
        if i == 0:
            out = [ ("", e) ]
        else:
            out.append( (lst[i-1], e ))
    return out

def scoreLink(link, mapping, b, q ):
    # if neither is in the mapping, score 0
    # if one is in the mapping, score 20 - log(b)
    # if both, score 100 - log(q)
    f, s = link
    if f in mapping and s in mapping:
        if (mapping[f], mapping[s]) in q:
            return 100 - q[(mapping[f], mapping[s])]
        else:
            return 100
    elif f in mapping:
        if mapping[f] in b:
            return 75 - b[mapping[f]]
        else:
            return 75
    elif s in mapping:
        if mapping[s] in b:
            return 75 - b[mapping[s]]
        else:
            return 75
    else:
        return 50

def scoreMapping( links, mapping, b, q ):
    # go through links in turn

    n = len(links)

    out = sum( map ( scoreLink,  links , [mapping for i in range(n)] , [b for i in range(n)], [q for i in range(n)]) )
    return out

def generateNewMappings(best, toAdd):
    out = []
    for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            pt = i + j

            if pt not in best.values():
                out.append(dict(best))
                out[-1][toAdd] = pt
            else:
                k = best.keys()
                if toAdd[0] == " ":
                    k = [kk for kk in best.keys() if kk[0] == " "]
                else:
                    k = [kk for kk in best.keys() if kk[2] == " "]
                ok = True
                for kk in k:
                    v = best[kk]
                    if v == pt:
                        ok = False
                        break
                if ok:
                    out.append(dict(best))
                    out[-1][toAdd] = pt

    return out

def translation( cipher, mapping ):
    out = ""
    for c in cipher:
        if c in mapping:
            out += mapping[c]
        else:
            out += "??"
    return out

def removeDuplicates(lst):
    out = []
    for i in lst:
        if i not in out:
            out.append(i)
    return out

def doTheDijkstra( ciphers, b, q ):
    lead = {}
    lead[0] = (10e20, None)
    sc = map(splitCipher,ciphers)
    links = map(createLinks, sc)
    csc = sc[0] + sc[1] + sc[2]
    ncsc = csc
    cc = collections.Counter(csc)
    ncsc = sorted(csc, key = lambda x: -cc[x]+4*random.random() )

    ncsc = removeDuplicates(ncsc)
    #random.shuffle(ncsc)
    mappings = {}
    mappings[0] = [(1.e20, {})]
    while mappings:
        # take the largest mapping index

        mx = min([max(mappings), 142])
        while not mappings[mx]:
            mx -= 1
        if mx+1 not in mappings:
            mappings[mx+1] = []
            lead[mx+1] = (1.e20, None)

        # ... and the best score within it
        mi, mn = min(enumerate(mappings[mx]), key=operator.itemgetter(1))

        s, best = mn
        #print mx, s, best
        #print translation(csc, best)
        leadFlag = False



        if ncsc[mx] not in best:
            for m in generateNewMappings(best, ncsc[mx]):
                scores =sum([scoreMapping(l, m, b, q) for l in links])

                if mx < 142:
                    mappings[mx+1].append( (scores, m) )
                if scores < lead[mx+1][0]:
                    lead[mx+1] = (scores, m)
                    for ii in sc:
                        print (mx, scores, translation(ii, m))
                    if mx == 142:
                        leadFlag = True


        else:
                # mappings.append( (s, i+1, m ))
                pass
        del mappings[mx][mi]
        if leadFlag or random.random() < 0.001:
            mk = mappings.keys()
            for mi in mk:
                if 143 in lead:
                    L = lead[143][0]
                else:
                    L = 1e20
                mappings[mi] = [m for m in mappings[mi] if m[0] < L]
                print (mi,":", len(mappings[mi]), end = "  ")
            print ()

        #tpr = ""
        #for m in mappings:
        #    tpr +=  "%d " % len(mappings[m])
        #print (tpr, end = '\r')
        #sys.stdout.write  (tpr +'\r')
        #sys.stdout.flush()
        #        r = random.random()
#         r = 0.
#         if r < 1.e-3 and mx > 140:
#             mk = mappings.keys()
#             mk.sort()
#             for ii in mk:
#                 print ii, len(mappings[ii]), lead[ii][0]
#             raw_input()

    raise NotImplementedError

ciphers = [" DUTM  UFVD  BHWK  RHEN  RDOY  LCVH  NRLD  QBOR  TMKN  TVDN  TMYH  TQSB  ECUH  LEML  RFLK  DMNH  YEOY  COMB  NLQS  TMKN  CDKM  NLOC  RQBH  RCNV  HPLE  DMNT  TWFL  RELY  QREH  SDLN  BQEW  EDLO  QREH  DUDN  NQOW  QREH  DCNT ",  " DUTM  CBFV  RQBH  MEOT  NKMQ  NDMO  SFWE  HLEK  RCUW  QREH  DMNT  RBUE  EKRS  QREH  CWRV  EQTY  SEPD  MNLE  ELLU  TMKN  WBEP  RISD  GMOS  RLEL ",  " EOCH  TQOL  BTOU  QREH  DVTM  NRLF  DUTN  DRSK  MYHT  DMNT  QKYD  BYCV  PDUR  BOHK  RYEL  TLOT  BDVH  BQRY  RYBK  POFW  DELY  SEPT  LKOM  TMKN  XREH  HWTY  NLHZ  CPQV  BDUH  NLQT  MDTU  DLQH  YKED  WBEP  ALST  SQYT  RAFW "]

bw, qw = getScores("ngrams2.csv", "ngrams4.csv")

mqv = max(qw.values())


best = doTheDijkstra(ciphers, bw, qw)
