## Sumologic Report Job Tool

This is a command-line tool that uses the [SumoLogic API](https://api.us2.sumologic.com/docs/#section/Getting-Started) to generate a PNG or PDF report of one or more dashboards. It uses a forked version of the [SumoLogic Python SDK](https://github.com/SumoLogic/sumologic-python-sdk) that I have updated to support the dashboard snapshots feature. If you would like to work off this project, you will need the include the alternate library located in **/lib/sumologic**.

<p align="right"></p>

### Usage

First, [download the latest release](https://github.com/AlexWaclawik/sumologic-report-tool/releases). To generate a report, you must edit the configuration file which is located in **/sumotool/config.ini**. See the section below on how to edit. * Once you have setup your config file, you can run **sumotool.exe** and it will produce a snapshot of your specified dashboard and will save it into **/reports/**.

<p align="right"></p>

### Configuration

**NOTE: The config file is CASE SENSITIVE!**

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
	
<p align="right"></p>