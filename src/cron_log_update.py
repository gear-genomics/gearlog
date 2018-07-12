#!/usr/bin/env python
import os
import logfunctions as lf
import settings as setti

CRNWS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PLOGPATH = os.path.join(CRNWS, "permalogs")
GEODBDV4 = os.path.join(CRNWS, "geodb", "geodb_IPv4.txt")
GEODBDV6 = os.path.join(CRNWS, "geodb", "geodb_IPv6.txt")

def cronupdate():
    if not os.path.exists(PLOGPATH):
        os.makedirs(PLOGPATH)
    if (os.path.isfile(GEODBDV4) != True) or (os.path.isfile(GEODBDV6) != True):
        print "Run ./src/update_GeoLite2.py first!"
        return
    ret = "ALL REQUESTS:\n_____________\n"
    pData = lf.cronLog2perm(setti.LOGDIR, setti.LOGBASE, PLOGPATH, GEODBDV4, GEODBDV6) 
    lf.add2permalog(PLOGPATH, pData["logList"])


if __name__ == "__main__":
    cronupdate()
