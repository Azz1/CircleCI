import croniter 
import csv 
import sys
from datetime import datetime, timedelta

def check_conflict(start_time, duration, cron_expressions_with_duration):
 end_time = start_time + duration
 max_span_minutes = 300 
 check_start_datetime = datetime.now() - timedelta(minutes=max_span_minutes)
 print("Check: " + str(start_time) + " for " + str(duration)) 
 
 for jobname, cron_expression, duration in cron_expressions_with_duration:
   iter = croniter.croniter(cron_expression, check_start_datetime) 	
   
   # Get the first run time on or after check start_time 
   first_run = iter.get_next(datetime) 
	
   while first_run < end_time:	
     #print("   Next run: " + jobname + " at " + str(first_run) + " for " + str(duration)) 
	 
     # Check for conflicts starting from the first potential run 
     if (first_run < start_time and first_run + duration > start_time) or (first_run < end_time and first_run  + duration >= end_time):
       return True, jobname, first_run, duration    # Conflict found
      
     # Get the next run time  
     first_run = iter.get_next(datetime) 
      	   
 return False, '', end_time, duration 		  		 # No conflict found

   
# Example usage 

if len(sys.argv) < 4:
  print("Usage: python CronChecker.py <start_time yyyy-mm-dd H24:MI:SS> <duration_minutes> <path_of_csv>")
  print('Example:\n     python CronChecker.py "2025-12-01 11:36:00" 12 Test.csv')
  exit()
  
  
#start_dt = datetime(2025, 12, 1, 11, 36, 0) 	# December 1st, 2025, 10:00 AM 
#duration = timedelta(minutes=12)

start_dt = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")
duration = timedelta(minutes=int(sys.argv[2]))
 
#cron_list_with_duration = [ ('job 1', '0 11 * * *', timedelta(minutes=30)), 	# Daily at 11:00 AM, runs for 30 minutes 
#                            ('job 2', '30 11 * * *', timedelta(minutes=5)), 	# Daily at 11:30 AM, runs for 30 minutes #
#							('job 3', '0 10 * * *', timedelta(minutes=10))		# Daily at 10:00 AM, runs for 10 minutes
#							] 

cron_list_with_duration = []
with open(sys.argv[3], newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cron_list_with_duration.append((row['JobName'], row['CronExpression'], timedelta(minutes=int(row['Duration']))))

isconf, jobname, tm, du = check_conflict(start_dt, duration, cron_list_with_duration)

if isconf: 
  print("Conflict detected! " + jobname + " at " + str(tm) + " for " + str(du) ) 
else: 
  print("No conflict detected.") 
