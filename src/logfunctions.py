#!/usr/bin/env python
import gzip
import os
import sys
import re
import hashlib
from datetime import datetime

import ip2integer as i2i
import settings as setti

lineformat = re.compile(r"""(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<remoteuser>[^ ]+) \[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] (\"(?P<requesttype>[a-z]+ )(?P<url>.+) (?P<protocol>http\/\d\.\d")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>[^"]+)["]) (["](?P<useragent>[^"]+)["])(?P<rest>.*)""", re.IGNORECASE)

def hashFileSHA256(fileName):
    sha256 = hashlib.sha256()
    with open(fileName,"rb") as hFile:
        for bBlock in iter(lambda: hFile.read(4096),b""):
            sha256.update(bBlock)
        return str(sha256.hexdigest())
    return "Error: Could not hash file: " + fileName

def convLogFormat(line,geodb):
    ret = ""
    da = re.search(lineformat, line)
    if da and da.group('statuscode') == "200":
        # First Ignore
        key = da.group('url')
        found = 0
        for fty in setti.IGNTYPE:
            if key.endswith(fty) == True:
                found = 1
        if found == 0:
            for trls in setti.TRACKLIST:
                if (key == trls[2]) or ((key.endswith('/') == True) and (key.rstrip('/') == trls[2]) and len(key) > 1) or ((trls[2].endswith('*') == True) and (key.startswith(trls[2].rstrip('*')) == True)):
                    intIP = i2i.ip2integer(da.group('ipaddress'))
                    country = "--,Unknown Country,"
                    # Worst way to find country
                    for bla in geodb:
                        if bla[0] <= intIP and bla[1] >= intIP:
                            country = bla[2] + "," + bla[3].rstrip() + ","
                            break
                    datetime_object = datetime.strptime(da.group('dateandtime')[:-6], '%d/%b/%Y:%H:%M:%S') # with py3 + %z')
                    ret += datetime_object.strftime('%Y.%m.%d,%H:%M:%S,') + '"' + trls[0] + '","' + trls[1] + '",'
                    ret += country + 'useragent="' + da.group('useragent') + '"'
    if len(ret) > 10:
        err = 0
    else:
        err = 1
    return {"err": err,"conv": ret}


def cronLog2perm(logdir, filebase, workdir, geoloc):
    zipFiles = []
    loadZip = []
    oldFiles = {}
    knownFiles = {}
    logList = []
    geodb = []
    with open(geoloc, "r") as geofile: 
        print "Load Geodata"
        last = -1
        for lin in geofile.readlines():
            start,end,cid,cnam = lin.split(",")
            if int(start) > int(end) or int(start) < last:
                print "Error in geoDB: ", start, " - ", end
            last = int(end)
            geodb.append([int(start),int(end),cid,cnam])

    for f in os.listdir(logdir):
        if f.startswith(filebase):
            if f.endswith(".gz"):
                zipFiles.append(os.path.join(logdir, f))

    # Hash new files an read only new
    if os.path.isfile(os.path.join(workdir, "knownFilesHash.txt.gz")) == True:
        pfile = gzip.open(os.path.join(workdir, "knownFilesHash.txt.gz"), "r")
        for li in pfile.readlines():
            oldFiles[li.rstrip()] = 1
        pfile.close()
    # Hash the current
    for f in zipFiles:
        fiHash = hashFileSHA256(f)
        knownFiles[fiHash] = 1
        if fiHash in oldFiles:
            print "Skiping known file: ", f
        else:
            loadZip.append(f)
            print "Loading new file: ", f
    # Save the list of hashes
    pfile = gzip.open(os.path.join(workdir, "knownFilesHash.txt.gz"), "w")
    for li in knownFiles:
        pfile.write(li + "\n")
    pfile.close()

    for f in loadZip:
        logfile = gzip.open(f)
        for l in logfile.readlines():
            rData = convLogFormat(l,geodb)
            if rData["err"] == 0:
              #  print rData["conv"]
                logList.append(rData["conv"])
        logfile.close()
    return {"logList": logList}

def add2permalog(ppath, logList):
    addData = {}
    for lin in logList:
        lar = lin.split('.')
        key = lar[0] + "_" + lar[1]
        if key in addData:
            addData[key].append(lin)
        else:
            addData[key] = [lin]

    for key,val in addData.items():
        if os.path.isfile(os.path.join(ppath, "perma_" + key + ".log.gz")) == True: 
            pfile = gzip.open(os.path.join(ppath, "perma_" + key + ".log.gz"), "r")
            for lin2 in pfile.readlines():
                addData[key].append(lin2.rstrip())
            pfile.close()
        srData = sorted(addData[key])
        pfile = gzip.open(os.path.join(ppath, "perma_" + key + ".log.gz"), "w")
        for lin3 in srData:
            pfile.write(lin3 + "\n")
        pfile.close()
        print key, val[0]


def log2dic(logdir, filebase):
    logList = []
    goodList = []
    failList = []
    for f in os.listdir(logdir):
        if f.startswith(filebase):
            if f.endswith(".gz"):
                logfile = gzip.open(os.path.join(logdir, f))
            else:
                logfile = open(os.path.join(logdir, f))

            for l in logfile.readlines():
                da = re.search(lineformat, l)
                if da:
                    logList.append([da.group('dateandtime'), da.group('url'), da.group('requesttype'), da.group('statuscode'), da.group('ipaddress'), da.group('useragent')])
                    goodList.append(l)
                else:
                    failList.append(l)
            logfile.close()
    return {"logList": logList,"failList": failList, "goodList": goodList}


def scoreStatus(logList):
    xstat = dict()
    for ent in logList:
        status = ent[3]
        if status in xstat:
            xstat[status] += 1
        else:
            xstat[status] = 1

    res = []
    for key,val in xstat.items():
        res.append([key, val])
    resi = sorted(res, key=lambda x: x[1], reverse=True)
    print "HTTP status code count\n----------------------"
    retVal = ""
    for x in resi:
        retVal += str(x[0]) +  "=>" +  str(x[1]) + "\n"
    return retVal

def scorePage(logList, nr):
    gPage = dict()
    ignPage = dict()
    trackPage = dict()
    untrPage = dict()
    bPage = dict()
    topNr = 10
    for ent in logList:
        page = ent[1]
        if ent[3] == "200":
            if page in gPage:
                gPage[page] += 1
            else:
                gPage[page] = 1
        else:
            if page in bPage:
                bPage[page] += 1
            else:
                bPage[page] = 1

    baPg = printList(bPage, "Non status 200 Urls:\n--------------------", nr)

    for key,val in gPage.items():
        found = 0
        for fty in setti.IGNTYPE:
            if key.endswith(fty) == True:
                found = 1
                ignPage[key] = gPage[key]
        if found == 0:
            foundKy = 0
            for trls in setti.TRACKLIST:
                if (key == trls[2]) or ((key.endswith('/') == True) and (key.rstrip('/') == trls[2]) and len(key) > 1) or ((trls[2].endswith('*') == True) and (key.startswith(trls[2].rstrip('*')) == True)):
                    foundKy = 1
                    nekey = '"' + trls[0] + '" - "' + trls[1] + '"'
                    if nekey in trackPage:
                        trackPage[nekey] += gPage[key]
                    else:
                        trackPage[nekey] = gPage[key]
                    break
            if foundKy == 0:
                untrPage[key] = gPage[key]

    ignPg = printList(ignPage, "Ignored by settings parameter:\n--------------------", nr) 
    unPg = printList(untrPage, "Untracked Pages:\n--------------------", nr)
    trPg = printList(trackPage, "Tracked Pages:\n--------------------", nr)

    return {"badPages": baPg, "ignoredPages": ignPg, "trackedPages": trPg, "untrackedPages": unPg}

def printList(ls, head, nr):
    res = []
    ret = head + "\n"
    for key,val in ls.items():
        res.append([key, val])
    resi = sorted(res, key=lambda x: x[1], reverse=True)
    if nr < 0:
        res2 = resi
    else:
        res2 = resi[:nr]
    for x in res2:
        ret += str(x[1]) + ": " + str(x[0]) + "\n"
    return ret

