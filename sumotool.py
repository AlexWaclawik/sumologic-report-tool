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
dashID = config['REPORT']['dashboardID']
actionType = config['REPORT']['actionType']
exportFormat = config['REPORT']['exportFormat']
timezone = config['REPORT']['timezone']
template = config['REPORT']['template']

def main():
    time.sleep(3)
    reportID = sumo.start_report(actionType, exportFormat, timezone, template, dashID)
    print("Report Job ID: " + reportID)
    keepGoing = True
    count = 0
    total = 43
    while (keepGoing):
        reportStatus = sumo.report_status(reportID)
        if reportStatus == "InProgress":
            progress(count, total)
            time.sleep(0.5)
            count += 1
            continue
        elif reportStatus == "Failed":
            print("ERROR: Report Job Has Failed")
            keepGoing = False
        elif reportStatus == "Success":
            print("SUCCESS: Report Job Complete")
            time.sleep(0.5)
            reportGenerate = sumo.report_result(reportID)
            rename_and_move()
            print("SUCCESS: Report Generation Complete")
            keepGoing = False


def progress(count, total):
    status = "Report Job In Progress..."
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def rename_and_move():
    filename = f_datetime + "-Report.png"
    src = str(cwd) + "\\result.png"
    dst = "../reports/"
    os.rename(src, filename)
    report = "./" + filename
    shutil.copy(report, dst)
    os.remove(filename)

if __name__ == "__main__":
    main()