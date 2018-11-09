#!/usr/bin/env python
import os
import gzip
import sys
import re
import argparse as argparse
import settings as setti
import logfunctions as lf

REPWS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LOGPATH = os.path.join(REPWS, "log_report")

def extractLogs(args):
    count = 0
    count_200 = 0
    for f in os.listdir(setti.LOGDIR):
        if f.startswith(setti.LOGBASE):
            if f.endswith(".gz"):
                logfile = gzip.open(os.path.join(setti.LOGDIR, f))
            else:
                logfile = open(os.path.join(setti.LOGDIR, f))

            for l in logfile.readlines():
                res = "Re FAIL"
                da = re.search(lf.lineformat, l)
                if da:
                    res = "Re success"


                if args['querry'] in l:
                    if args['date'] in l:
                        print l + res
                        count += 1
                        if da.group('statuscode') == '200':
                            count_200 += 1

            logfile.close()
    print "\nFound " + str(count) + " lines (" +  str(count_200) + " with status code 200)!\n"

if __name__ == "__main__":
    pars = argparse.ArgumentParser(description='Querry the log files')
    pars.add_argument('-q','--querry', help='String to be found in each log line', required=True)
    pars.add_argument('-d','--date', help='Date to be found in each log line', required=True)
    args = vars(pars.parse_args())
    extractLogs(args)

