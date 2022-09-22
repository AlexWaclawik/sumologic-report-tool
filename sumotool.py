# SumoLogic Report Tool
# Created by Alex Waclawik
# Version 1.2.1

import sys
import time
import configparser
import shutil
import os
import pathlib
from datetime import datetime
from lib.sumologic import SumoLogic

# sets the path 
cwd = pathlib.Path().resolve()

# initialize configparser
config = configparser.ConfigParser()
config.read("config.ini")
# initialize date and time, as well as declare date and time vars
now = datetime.now()
c_date = now.strftime("%y/%m/%d")
c_time = now.strftime("%H:%M:%S")
f_datetime = now.strftime("%y%m%d-%H%M%S")
print("SumoLogic SDK")
print("The date is " + c_date + " and the time is currently " + c_time)

args = sys.argv
accessID = config['API']['accessID']
accessKey = config['API']['accessKey']
sumo = SumoLogic(accessID, accessKey)

def main():
    time.sleep(1)
    # get number of sections in config to get number of reports
    sections = config.sections()
    num_of_reports = len(sections)
    for x in range(0, num_of_reports - 1):
        # check if report is enabled
        reportName = 'REPORT_' + str(x)
        reportStatus = config[reportName].getboolean('enabled')
        if reportStatus == True:
            # get the report job parameters from the config file
            name = config[reportName]['name']
            print("\n|--< Starting Job for '" + name + "' >--|")
            dashID = config[reportName]['dashboardID']
            actionType = config[reportName]['actionType']
            exportFormat = config[reportName]['exportFormat']
            timezone = config[reportName]['timezone']
            template = config[reportName]['template']
            # start the report job
            try:
                reportID = sumo.start_report(actionType, exportFormat, timezone, template, dashID)
            except ConnectionError:
                print("ERROR: Connection Aborted")
            # wait for the report job to finish
            get_panel(reportID)
            # rename and move the file to its final location
            savedFile = rename_and_move(name, exportFormat)
            print("SUCCESS: The Panel Report '" + savedFile + "' has been saved")
            time.sleep(1)
        else:
            continue

def get_panel(reportID):
    print("Report Job ID: " + reportID)
    keepGoing = True
    start_time = time.time()
    while (keepGoing):
        # check the status of the report job
        reportStatus = sumo.report_status(reportID)
        if reportStatus == "InProgress":
            # keeps track of the elapsed time, average is around 30 seconds
            elap_time = round((time.time() - start_time), 2)
            sys.stdout.write('...Job In Progress...    Elapsed Time: %s\r' % (elap_time))
            sys.stdout.flush()
            time.sleep(0.5)
            continue
        elif reportStatus == "Failed":
            print("ERROR: Report Job Has Failed")
            keepGoing = False
        elif reportStatus == "Success":
            # save the report and return
            reportGenerate = sumo.report_result(reportID)
            time.sleep(0.5)
            print("\nSUCCESS: Report Job Complete")
            keepGoing = False

def rename_and_move(name, format):
    # determine the format
    if format == "Png":
        fileExt = ".png"
    elif format == "Pdf":
        fileExt = ".pdf"
    # concatenate the output filename
    filename = f_datetime + "_" + name + "_Report" + fileExt
    # specificy source and destination
    src = str(cwd) + "\\result.png"
    dst = "../reports/"
    # rename the file then copy it over to new destination
    os.rename(src, filename)
    report = "./" + filename
    shutil.copy(report, dst)
    # remove the source file
    os.remove(filename)
    return(filename)

if __name__ == "__main__":
    main()