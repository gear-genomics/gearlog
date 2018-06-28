#!/usr/bin/env python
import os
import logfunctions as lf
import settings as setti

REPWS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LOGPATH = os.path.join(REPWS, "log_report")

def createReport():
    if not os.path.exists(LOGPATH):
        os.makedirs(LOGPATH)
    with open(os.path.join(LOGPATH, "_report.txt"), "w") as report:
        ret = "ALL REQUESTS:\n_____________\n"
        pData = lf.log2dic(setti.LOGDIR, setti.LOGBASE) 
        ret += "Read Lines: " + str(len(pData["logList"])) + "\n"
        ret += "Unreadable Lines: " + str( len(pData["failList"])) + "\n"
        ret += "--> See all unreadable lines in:\n    " + os.path.join(LOGPATH, "failed_lines.txt") + "\n"
        with open(os.path.join(LOGPATH, "failed_lines.txt"), "w") as err:
            errData = pData["failList"]
            for x in errData:
                err.write(x)
        report.write(ret + "\n")
        print ret

        ret = lf.scoreStatus(pData["logList"])
        report.write(ret + "\n")
        print ret

        sData = lf.scorePage(pData["logList"], 20)
        ret = "The top 20 tracked pages from:\n    " + os.path.join(LOGPATH, "tracked_pages.txt") + "\n"
        ret += sData["trackedPages"] +  "\n"
        ret += "The top 20 untracked pages from:\n    " + os.path.join(LOGPATH, "untracked_pages.txt") + "\n"
        ret += sData["untrackedPages"] +  "\n"
        ret += "The top 20 ignored pages from:\n    " + os.path.join(LOGPATH, "ignored_pages.txt") + "\n"
        ret += sData["ignoredPages"] +  "\n"
        ret += "The top 20 bad pages from:\n    " + os.path.join(LOGPATH, "non_status_200_pages.txt") + "\n"
        ret += sData["badPages"] + "\n"
        report.write(ret + "\n")
        print ret
        with open(os.path.join(LOGPATH, "tracked_pages.txt"), "w") as trackpage:
            with open(os.path.join(LOGPATH, "untracked_pages.txt"), "w") as untrpage:
                with open(os.path.join(LOGPATH, "ignored_pages.txt"), "w") as ignpage:
                    with open(os.path.join(LOGPATH, "non_status_200_pages.txt"), "w") as badpage:
                        sData = lf.scorePage(pData["logList"], -1)
                        trackpage.write(sData["trackedPages"])
                        untrpage.write(sData["untrackedPages"])
                        ignpage.write(sData["ignoredPages"])
                        badpage.write(sData["badPages"])



if __name__ == "__main__":
    createReport()
