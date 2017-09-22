from math import log
qf = open("english_quadgrams.txt",'r')
l = qf.readlines()
quads = {}
for i in l:
    q, n = i.split(" ")
    quads[q] = log(float(n))
    
df = open("english_bigrams.txt",'r')
l = df.readlines()
big = {}
for i in l:
    b, n = i.split(" ")
    big[b] = log(float(n))
    
lst = [(2*quads[q] - big[q[:2]] - big[q[2:]],q) for q in quads]
lst.sort()


print "\n".join(["%s %f" % (i[1],i[0]) for i in lst[-20:]])