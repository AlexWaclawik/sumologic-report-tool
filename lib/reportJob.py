class ReportJob(object):

    def __init__(self, Name, DashID, ActionType, ExportFormat, TimeZone, Template, ReportName):
        self.name = Name
        self.dashID = DashID
        self.actionType = ActionType
        self.exportFormat = ExportFormat
        self.timezone = TimeZone
        self.template = Template
        self.reportName = ReportName
        self.reportID = None
        self.finished = False
        self.failed = False




