#! /usr/bin/env python

import os
import uuid
import re
import subprocess
import argparse
import json
import gzip
from datetime import datetime, timedelta
from subprocess import call
from flask import Flask, send_file, flash, send_from_directory, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
GLOGWS = os.path.dirname(os.path.abspath(__file__))

app.config['GEARLOG'] = os.path.join(GLOGWS, "..")
app.config['BASEURL'] = '/gearlog'
app.static_folder = app.static_url_path = os.path.join(GLOGWS, "../client/static")

@app.route('/api/v1/upload', methods=['POST'])
def generate():
    fList = [] # Files to read
    data = [] # All relevant data
    keyDic = {} # The primary keys from data
    keyList = [] # The primary keys in a list
    secDic = {} # The secondary keys from data pointing to array position
    secList = [] # The List of the secondary keys in correct order
    dateList = {} # The dates from data pointing to array position
    resData = [] # Twodimensional array with all results
    countries = {} # Count the countries
    countryNames = {} # Translate countries
    resCountry = [] # Twodimensional array with all results

    try:
        primKey = request.form['primKey']
        dateStart = request.form['dateStart']
        dateEnd  = request.form['dateEnd']
    except KeyError:
        return jsonify(errors = [{"title": "Error: Required input keys missing to process the request."}]), 400
    if datetime.now() < datetime.strptime(dateEnd, "%Y-%m-%d"):
        dateEnd = datetime.now().strftime('%Y-%m-%d')
    if datetime.strptime(dateEnd, "%Y-%m-%d") < datetime.strptime(dateStart, "%Y-%m-%d"):
        return jsonify(errors = [{"title": "Error: Start time later as end time."}]), 400
    spanDays = abs((datetime.strptime(dateEnd, "%Y-%m-%d") - datetime.strptime(dateStart, "%Y-%m-%d")).days)

    # Only load data of relevance into data dic
    monthStart = dateStart[:-3]
    monthEnd = dateEnd[:-3]
    fList.append(monthStart)
    i = 0
    while monthStart != monthEnd and i < 120:
        i += 1
        yyyy,mm = monthStart.split('-')
        iMM = int(mm) + 1
        if iMM < 10:
            mm = '0' + str(iMM)
        elif iMM < 13:
            mm = str(iMM)
        elif iMM > 12:
            mm = '01'
            yyyy = str(int(yyyy) + 1)
        monthStart = yyyy + "-" + mm
        fList.append(monthStart)

    cptStart = datetime.strptime(dateStart, "%Y-%m-%d")
    cptEnd = datetime.strptime(dateEnd, "%Y-%m-%d")
    for f in fList:
        fil = f.replace("-", "_")
        endFile = os.path.join(GLOGWS, "../permalogs", "perma_" + fil + ".log.gz")
        if os.path.isfile(endFile) == True:
            logfile = gzip.open(endFile)
            for l in logfile.readlines():
                linArr = l.split(',')
                keyDic[linArr[2]] = 1
                lTime = datetime.strptime(linArr[0], "%Y.%m.%d")
                if linArr[2] == '"' + primKey + '"' and cptStart < lTime and cptEnd > lTime:
                    data.append(l)
            logfile.close()
    for key,val in keyDic.items():
        keyList.append(key.strip('"'))

    # Process the data
    ## Collect secondary keys
    for l in data:
        linArr = l.split(',')
        secDic[linArr[3]] = 1
    k = 0; # 0 is the date
    secList.append("Date")
    for key,val in secDic.items():
        k += 1
        secList.append(key)
        secDic[key] = k
    resData.append(secList)

    ## Get a List of the dates 
    if spanDays < 100:
        cptStart = datetime.strptime(dateStart, "%Y-%m-%d")
        cptEnd = datetime.strptime(dateEnd, "%Y-%m-%d")
        cptI = cptEnd
        resData.append([cptI.strftime('%Y.%m.%d'), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        dateList[cptI.strftime('%Y.%m.%d')] = 1
        i = 1
        while cptEnd >= cptStart and i < 120:
            i += 1
            cptI -= timedelta(hours=24)
            resData.append([cptI.strftime('%Y.%m.%d'), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dateList[cptI.strftime('%Y.%m.%d')] = i
        for l in data:
            linArr = l.split(',')
            resData[dateList[linArr[0]]][secDic[linArr[3]]] += 1
    else:
        monthStart = dateStart[:-3]
        monthEnd = dateEnd[:-3]
        resData.append([monthEnd, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        dateList[monthEnd.replace('-','.')] = 1
        i = 1
        while monthStart != monthEnd and i < 1200:
            i += 1
            yyyy,mm = monthEnd.split('-')
            iMM = int(mm) - 1
            if iMM <= 0:
                mm = '12'
                yyyy = str(int(yyyy) - 1)
            elif iMM < 10:
                mm = '0' + str(iMM)
            elif iMM < 13:
                mm = str(iMM)
            monthEnd = yyyy + "-" + mm
            resData.append([yyyy + "-" + mm, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            dateList[yyyy + "." + mm] = i
        for l in data:
            linArr = l.split(',')
            resData[dateList[linArr[0][:-3]]][secDic[linArr[3]]] += 1

    ## Count the countries
    for l in data:
        linArr = l.split(',')
        countryNames[linArr[4]] = linArr[5]
        if linArr[4] in countries:
            countries[linArr[4]] += 1
        else:
            countries[linArr[4]] = 1
    for key,val in countries.items():
        resCountry.append([countryNames[key].strip('"'),val])
    resCountSrt = sorted(resCountry, key=lambda x: x[1], reverse=True)

    return jsonify(data = {"primKeys": keyList, "counts": resData, "countries": resCountSrt})

@app.route('/')
def root():
    return send_from_directory(os.path.join(GLOGWS, "../client"),"index.html"), 200


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=3300, debug = True, threaded=True)
