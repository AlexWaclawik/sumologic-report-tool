import sys
import time

from datetime import datetime
from pyfiglet import Figlet
from lib.sumologic import SumoLogic

now = datetime.now()
f = Figlet(font='big')
print(f.renderText('SumoLogic SDK'))
c_datetime = now.strftime("%y/%m/%d %H:%M:%S")
print(c_datetime)

args = sys.argv
sumo = SumoLogic("ACCESSID", "ACCESSKEY")
dashID = "DASHBOARDID"


def main():

    time.sleep(3)
    reportID = sumo.start_report()
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
            keepGoing = False

    reportGenerate = sumo.report_result(reportID)
    print(reportGenerate)


def get_time():
    t = now.strftime("%H:%M:%S")
    return(t)

if __name__ == "__main__":
    main()