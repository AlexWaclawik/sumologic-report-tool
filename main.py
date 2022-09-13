import sys
import time
import configparser

from datetime import datetime
from pyfiglet import Figlet
from lib.sumologic import SumoLogic

config = configparser.ConfigParser()
config.read("config.ini")
now = datetime.now()
f = Figlet(font='big')
print(f.renderText('SumoLogic SDK'))
c_datetime = now.strftime("%y/%m/%d_%H:%M:%S")
print(c_datetime)

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
    while (keepGoing):
        reportStatus = sumo.report_status(reportID)
        if reportStatus == "InProgress":
            print("Report Job In Progress...")
            time.sleep(5)
            continue;
        elif reportStatus == "Failed":
            print("ERROR: Report Job Has Failed")
            keepGoing = False
        elif reportStatus == "Success":
            print("SUCCESS: Report Job Complete")
            reportGenerate = sumo.report_result(reportID)
            print(reportGenerate)
            keepGoing = False


def get_time():
    t = now.strftime("%H:%M:%S")
    return(t)

if __name__ == "__main__":
    main()