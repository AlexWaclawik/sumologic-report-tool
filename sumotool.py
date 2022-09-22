# SumoLogic Report Tool
# Created by Alex Waclawik
# Version 1.3.0

import sys
import time
import configparser
import shutil
import os
import pathlib
from datetime import datetime
from lib.sumologic import SumoLogic
from bin.reportJob import ReportJob

# sets the path 
cwd = pathlib.Path().resolve()

# initialize configparser
config = configparser.ConfigParser()
config.read("config.ini")
sections = config.sections()
report_num = (len(sections) - 1)
# initialize date and time, as well as declare date and time vars
now = datetime.now()
c_date = now.strftime("%y/%m/%d")
c_time = now.strftime("%H:%M:%S")
f_datetime = now.strftime("%y%m%d-%H%M%S")
print("SumoLogic Report Tool 1.3.0")
print("The date is " + c_date + " and the time is currently " + c_time)

# establish API connection
args = sys.argv
accessID = config['API']['accessID']
accessKey = config['API']['accessKey']
sumo = SumoLogic(accessID, accessKey)

# list of job report objects
job_arr = []

def main():
    init_reports()
    start_reports()
    do_jobs()
    rename_and_move()

def init_reports():
    for x in range(0, report_num):
        reportName = 'REPORT_' + str(x)
        name = config[reportName]['name']
        dashID = config[reportName]['dashboardID']
        actionType = config[reportName]['actionType']
        exportFormat = config[reportName]['exportFormat']
        timezone = config[reportName]['timezone']
        template = config[reportName]['template']
        job_arr.append(ReportJob(name, dashID, actionType, exportFormat, timezone, template, reportName))

def start_reports():
    for x in range(0, report_num):
        tempID = sumo.start_report(job_arr[x].actionType, job_arr[x].exportFormat, job_arr[x].timezone, job_arr[x].template, job_arr[x].dashID)
        job_arr[x].reportID = tempID

def do_jobs():
    print("\n|--< Starting Jobs >--|")
    running_jobs = len(job_arr)
    start_time = time.time()
    keepGoing = True
    while (keepGoing):
        for x in range(0, report_num):
            status = sumo.report_status(job_arr[x].reportID)
            if job_arr[x].finished == True or job_arr[x].failed == True:
                time.sleep(0.5)
                continue
            elif status == "InProgress":
                elap_time = round((time.time() - start_time), 2)
                sys.stdout.write('...%s Jobs In Progress...    Elapsed Time: %s\r' % (running_jobs, elap_time))
                sys.stdout.flush()
                time.sleep(0.5)
            elif status == "Failed":
                job_arr[x].failed = True
                running_jobs -= 1
                time.sleep(0.5)
            elif status == "Success":
                job_arr[x].finished = True
                running_jobs -= 1
                time.sleep(0.5)
        if running_jobs == 0:
            keepGoing = False
    print("\n|--< Jobs Finished >--|")

def rename_and_move():
    for x in range(0, report_num):
        # generate the snapshot
        generate = sumo.report_result(job_arr[x].reportID)
        # determine the format
        if job_arr[x].exportFormat == "Png":
            fileExt = ".png"
        elif job_arr[x].exportFormat == "Pdf":
            fileExt = ".pdf"
        # concatenate the filename and specify source and destination
        filename = f_datetime + "_" + job_arr[x].name + "_Report" + fileExt
        src = str(cwd) + "\\result.png"
        dst = "../reports/"
        # rename the file, copy to new destination, then remove source
        os.rename(src, filename)
        report = "./" + filename
        # I have it sleep after copy and delete functions otherwise it will move to fast
        # better solution is to run on single thread
        shutil.copy(report, dst)
        time.sleep(3)
        os.remove(filename)
        time.sleep(3)
        print("\nSUCCESS: The Panel Report '" + filename + "' has been saved")

if __name__ == "__main__":
    main()