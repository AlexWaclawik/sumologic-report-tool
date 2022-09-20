## Sumologic Report Job Tool

This is a command-line tool that uses the [SumoLogic Python SDK](https://github.com/SumoLogic/sumologic-python-sdk) and [SumoLogic API](https://api.us2.sumologic.com/docs/#section/Getting-Started) to generate a PNG or PDF report of one or more dashboards. It is intended as an automated task to be ran on a schedule.

### Usage

To start, you must edit the configuration file which is located in **/sumotool/config.ini**. **NOTE: The config file is CASE SENSITIVE!** Once you have setup your config file, you can run **sumotool.exe** and it will produce a snapshot of your specified dashboard and will save it into **./reports/**.

### Configuration
The first header is where you will put your API access ID and access key:
```ini
[API]
version = 1.2
accessID = YOUR_ID_HERE
accessKey = YOUR_KEY_HERE
```

The second and following headers are where you will put your jobs:
```ini
[REPORT_0]
```
* The name has to be in the format of **[REPORT_NUMBER]** starting with zero.
* Each report has to be in sequential order.
* You can have as many reports as you want.
```ini
enabled = true
```
* Tells the tool whether to ignore this report or not. Useful for troubleshooting issues.
```ini
name = My_Panel
```
* Name of the panel. This is what will be used to generate the name of the report.
* Do not use any restricted file name characters ('/', '\', ':', etc)
```ini
dashboardID = YOUR_DASH_ID_HERE
```
* ID of the dashboard to generate the report for.
```ini
actionType = DirectDownloadReportAction
```
* Type of action to be done. Currently only one action type is supported.
```ini
exportFormat = Png
```
* Specifices the export format of the report:
	- PDF -> **Pdf**
	- PNG -> **Png**
```ini
timezone = America/New_York
```
* Specifies the timezone present on the dashboard report.
* [Uses IANA Format.](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)
```ini
template = DashboardTemplate
```
* Specifices the template type that will be used:
	- Default -> **DashboardTemplate**
	- Printer-Friendly -> **DashboardReportModeTemplate**

### Credits

1. [SumoLogic Python SDK](https://github.com/SumoLogic/sumologic-python-sdk)
2. [Pyfiglet](https://github.com/pwaller/pyfiglet)