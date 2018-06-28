#!/usr/bin/env python

def ip2integer(ip):
    blck = map(int, ip.split('.'))
    return (16777216 * blck[0]) + (65536 * blck[1]) + (256 * blck[2]) + blck[3] 

def integer2ip(i):
    blck1 = int(i / 16777216) % 256
    blck2 = int(i / 65536) % 256
    blck3 = int(i / 256) % 256
    blck4 = int(i) % 256
    return '%(blck1)s.%(blck2)s.%(blck3)s.%(blck4)s' % locals()

def calcMask(ip):
    msk = ip.split('/')
    if int(msk[1]) > 31:
        return [ip, ip2integer(msk[0]), ip2integer(msk[0])]
    nbit = int(msk[1])
    hbit = 32 - nbit
    sMask = ('1'*nbit).zfill(32)[::-1] # [::-1] does reverse the string
    nMask = int(sMask,2)
    hMask = '1'*hbit
    nHigh = int(hMask,2)
    nIp = ip2integer(msk[0])
    lowIp = nIp & nMask
    highIp = nIp | nHigh
    return [ip, lowIp, highIp]
