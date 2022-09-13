## Sumologic Report Job Tool

This is a command-line tool that uses the [SumoLogic Python SDK](https://github.com/SumoLogic/sumologic-python-sdk) to generate a dashboard report. For more information on the SumoLogic API, [view the documentation here.](https://api.us2.sumologic.com/docs/#section/Getting-Started)

### Usage

In *config.ini* you can change several values that will allow you to access your SumoLogic API. They are as follows:

1. accessID
	* Your API Access ID.
2. accessKey
	* Your API Access Key.
3. dashboardID
	* The ID of the dashboard you want to generate a report on.
4. actionType
	* Only one action type right now, so leave this be.
5. exportFormat
	* Png
	* Pdf
6. timezone
	* [IANA Format](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)
7. template
	* "DashboardTemplate" is the default.
	* "DashboardReportModeTemplate" is a printer-friendly version.
