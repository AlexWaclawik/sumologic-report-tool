### 1. Report Job Class:

	name = config[reportName]['name']
	dashID = config[reportName]['dashboardID']
	actionType = config[reportName]['actionType']
	exportFormat = config[reportName]['exportFormat']
	timezone = config[reportName]['timezone']
	template = config[reportName]['template']

    reportID = string
    savedFile = string

### 2. Create An Array of Report Job Classes
    
    job_arr = []
	Access each element to get instance of report job

### 3. Start Job Report for Each Class
    
    for x = 0; x < sizeof(job_arr):
        job_arr[x].reportID = sumo.start_report(job_arr[x].actionType, etc etc)

### 4. Run Through The Jobs

    arr_size = sizeof report job array
    while true:
        jobs_running = sizeof(job_arr)
        for x = 0; x < sizeof(job_arr):
            if number_of_jobs == 0:
                EXIT WHILE LOOP
            else: 
                first check if we skip this specific instance (we do this if it is finished or failed)
                check report of 'REPORT_x'
                if in progress:
                    output X jobs in progress and time
                elif failed:
                    mark the instance to be skipped
                elif success: 
                    mark the instance as finished
                    number_of_completed =- 1

### 4. Then just call rename_and_move() for every instance

    for x = 0; x < sizeof(job_arr):
        job_arr[x].savedFile = rename_and_move(job_arr[x].name, job_arr[x].exportFormat)
        print("SUCCESS: The Panel Report '" + job_arr[x].savedFile + "' has been saved")