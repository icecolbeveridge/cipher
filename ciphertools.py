# ciphertools.py
import math

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

ciphers = [" DUTM  UFVD  BHWK  RHEN  RDOY  LCVH  NRLD  QBOR  TMKN  TVDN  TMYH  TQSB  ECUH  LEML  RFLK  DMNH  YEOY  COMB  NLQS  TMKN  CDKM  NLOC  RQBH  RCNV  HPLE  DMNT  TWFL  RELY  QREH  SDLN  BQEW  EDLO  QREH  DUDN  NQOW  QREH  DCNT ",  " DUTM  CBFV  RQBH  MEOT  NKMQ  NDMO  SFWE  HLEK  RCUW  QREH  DMNT  RBUE  EKRS  QREH  CWRV  EQTY  SEPD  MNLE  ELLU  TMKN  WBEP  RISD  GMOS  RLEL ",  " EOCH  TQOL  BTOU  QREH  DVTM  NRLF  DUTN  DRSK  MYHT  DMNT  QKYD  BYCV  PDUR  BOHK  RYEL  TLOT  BDVH  BQRY  RYBK  POFW  DELY  SEPT  LKOM  TMKN  XREH  HWTY  NLHZ  CPQV  BDUH  NLQT  MDTU  DLQH  YKED  WBEP  ALST  SQYT  RAFW "]

bw, qw = getScores("ngrams2.csv", "ngrams4.csv")

sc = map(splitCipher,ciphers)
links = map(createLinks, sc)
