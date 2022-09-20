import sys
import time
import configparser
import shutil
import os
import pathlib
from datetime import datetime
from pyfiglet import Figlet
from lib.sumologic import SumoLogic

cwd = pathlib.Path().resolve()

config = configparser.ConfigParser()
config.read("config.ini")
now = datetime.now()
c_date = now.strftime("%y/%m/%d")
c_time = now.strftime("%H:%M:%S")
f_datetime = now.strftime("%y%m%d-%H%M%S")
f = Figlet(font='smslant')
print(f.renderText('SumoLogic SDK'))
print("The date is " + c_date + " and the time is currently " + c_time)

args = sys.argv
accessID = config['API']['accessID']
accessKey = config['API']['accessKey']
sumo = SumoLogic(accessID, accessKey)

def main():
    time.sleep(1)
    sections = config.sections()
    num_of_reports = len(sections) - 1
    for x in range(0, num_of_reports):
        reportName = 'REPORT_' + str(x)
        reportStatus = config[reportName].getboolean('enabled')
        if reportStatus == True:
            name = config[reportName]['name']
            print("\n|--< Starting Job for '" + name + "' >--|")
            dashID = config[reportName]['dashboardID']
            actionType = config[reportName]['actionType']
            exportFormat = config[reportName]['exportFormat']
            timezone = config[reportName]['timezone']
            template = config[reportName]['template']
            reportID = sumo.start_report(actionType, exportFormat, timezone, template, dashID)
            get_panel(reportID)
            savedFile = rename_and_move(name, exportFormat)
            print("SUCCESS: The Panel Report '" + savedFile + "' has been saved")
        else:
            continue

def get_panel(reportID):
    print("Report Job ID: " + reportID)
    keepGoing = True
    start_time = time.time()
    while (keepGoing):
        reportStatus = sumo.report_status(reportID)
        if reportStatus == "InProgress":
            elap_time = round((time.time() - start_time), 2)
            sys.stdout.write('...Job In Progress...    Elapsed Time: %s\r' % (elap_time))
            sys.stdout.flush()
            time.sleep(0.5)
            continue
        elif reportStatus == "Failed":
            print("ERROR: Report Job Has Failed")
            keepGoing = False
        elif reportStatus == "Success":
            reportGenerate = sumo.report_result(reportID)
            time.sleep(0.5)
            print("\nSUCCESS: Report Job Complete")
            keepGoing = False

def rename_and_move(name, format):
    if format == "Png":
        fileExt = ".png"
    elif format == "Pdf":
        fileExt = ".pdf"
    filename = f_datetime + "_" + name + "_Report" + fileExt
    src = str(cwd) + "\\result.png"
    dst = "../reports/"
    os.rename(src, filename)
    report = "./" + filename
    shutil.copy(report, dst)
    os.remove(filename)
    return(filename)

if __name__ == "__main__":
    main()