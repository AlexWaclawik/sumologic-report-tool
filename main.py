import sys
import time

from datetime import datetime
from pyfiglet import Figlet
from lib.sumologic import SumoLogic

now = datetime.now()
f = Figlet(font='big')
print(f.renderText('SumoLogic SDK'))
c_datetime = now.strftime("%y/%m/%d_%H:%M:%S")
print(c_datetime)

args = sys.argv
sumo = SumoLogic("ACCESS-ID", "ACCESS-KEY")
dashID = "DASHBOARD-ID"
actionType="DirectDownloadReportAction"
exportFormat="Png"
timezone="America/New_York" 
template="DashboardTemplate"


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
