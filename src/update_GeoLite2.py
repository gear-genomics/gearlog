#!/usr/bin/env python
import os
import subprocess
import zipfile
import ip2integer as i2i

from subprocess import call

DATABASE = "http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip"
IP4FILE = "GeoLite2-Country-Blocks-IPv4.csv"
IP6FILE = "GeoLite2-Country-Blocks-IPv6.csv"
LOC_FILE = "GeoLite2-Country-Locations-en.csv"

STATWS = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
GEODBD = os.path.join(STATWS, "geodb")
GEOLIT = os.path.join(STATWS, "geodb", "geolite")

def getDatabase():
    print("Downloading Database...")
    if not os.path.exists(GEODBD):
        os.makedirs(GEODBD)
    if not os.path.exists(GEOLIT):
        os.makedirs(GEOLIT)
    return_code = call(["wget", "-O", os.path.join(GEOLIT, "GeoLite2-Country-CSV.zip"), DATABASE])
    if not return_code == 0:
        print "Error downloading Database: ", return_code
        return
    print("Unpacking Database...")
    zip_ref = zipfile.ZipFile(os.path.join(GEOLIT, "GeoLite2-Country-CSV.zip"), 'r')
    filelist = zip_ref.namelist()
    prefolder = filelist[0].split('/')
    zip_ref.extract(prefolder[0] + "/" + IP4FILE, GEOLIT)
    zip_ref.extract(prefolder[0] + "/" + IP6FILE, GEOLIT)
    zip_ref.extract(prefolder[0] + "/" + LOC_FILE, GEOLIT)
#   zip_ref.extractall("geolite")
    zip_ref.close()
    print("Processing Database...")
    with open(os.path.join(GEOLIT, prefolder[0], LOC_FILE), "r") as loci:
        fCont = loci.readlines()
        fCont.pop(0) # Away the header
        locDic = {}
        for lin in fCont:
            lLis = lin.split(',')
            if lLis[5] == '':
                locDic[lLis[0]] = "--," + lLis[3]
            else:
                locDic[lLis[0]] = lLis[4] + "," + lLis[5]

        with open(os.path.join(GEODBD, "geodb.txt"), "w") as geodb:
            with open(os.path.join(GEOLIT, prefolder[0], IP4FILE), "r") as ip4file:
                ip4all = ip4file.readlines()
                ip4all.pop(0) # Away the header
                for lin in ip4all:
                    lLis = lin.split(',')
                    netWork = i2i.calcMask(lLis[0])
                    if lLis[1] in locDic:
                        geodb.write(str(netWork[1]) + "," + str(netWork[2]) + "," + locDic[lLis[1]] + "\n")
                    elif lLis[2] in locDic:
                        geodb.write(str(netWork[1]) + "," + str(netWork[2]) + "," + locDic[lLis[2]] + "\n")
                    else:
                        geodb.write(str(netWork[1]) + "," + str(netWork[2]) + ",--,Unknown Country\n" )
                print "Done."


if __name__ == "__main__":
    # python2 raw_input / python3 input:
    resp = raw_input("Download Database from maxmind.com? [Yes/No]: ")
    if resp.lower().startswith("y"):
        getDatabase()

