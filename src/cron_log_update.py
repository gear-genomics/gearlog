#!/usr/bin/env python
import os
import logfunctions as lf
import settings as setti

CRNWS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PLOGPATH = os.path.join(CRNWS, "permalogs")
GEODBD = os.path.join(CRNWS, "geodb", "geodb.txt")

def cronupdate():
    if not os.path.exists(PLOGPATH):
        os.makedirs(PLOGPATH)
    ret = "ALL REQUESTS:\n_____________\n"
    pData = lf.cronLog2perm(setti.LOGDIR, setti.LOGBASE, PLOGPATH, GEODBD) 
    lf.add2permalog(PLOGPATH, pData["logList"])


if __name__ == "__main__":
    cronupdate()
