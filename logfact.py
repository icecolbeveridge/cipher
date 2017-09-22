from math import log, exp

global FACT
FACT = { 0: 0., 1: 0. }

def logfact(n):
    if n < 0 or n != int(n):
        raise ValueError
    if n in FACT:
        return FACT[n]
    else:
        return log(n) + logfact(n-1)

logfact(30)