import psycopg2
import pandas as pd
import boto3
from configparser import ConfigParser

#reading the raw dataset calldetails and call log"
call_details = pd.read_csv('call details.csv')
call_log = pd.read_csv('call log.csv')

print('successful')

### CLEANING THE DATASET
# CREATING A COPY OF THE 2 DATASET

call_details_copy = call_details.copy()
call_log_copy = call_log.copy()

# rename column header
call_details_copy.rename(columns= {'callID':'call_id', 'callDurationInSeconds': 'duration_of_calls_in_sec', 'agentsGradeLevel': 'agents_grade_level', 'callType': 'call_type', 'callEndedByAgent':'call_ended_by_agent'}, inplace=True)

print('successful')

#data cleaning:
# removing the '-' in "in-bound"
call_details_copy['call_type'] = call_details_copy['call_type'].str.replace('-','')

# capitalizing the first letter and changing the rem to lower case
call_details_copy['call_type']= call_details_copy['call_type'].str.lower().str.capitalize()

# removing white spaces
call_details_copy['call_type'] = call_details_copy['call_type'].str.strip('  ')

# create a copy dataframe df2_copy

call_log_copy = call_log.copy()
#fill nan values

call_log_copy['resolutionDurationInHours'] = call_log_copy['resolutionDurationInHours'].fillna(value=0)

call_log_copy['assignedTo'] = call_log_copy['assignedTo'].fillna(call_log_copy['agentID'])

#change assignedto datatype from float to int
call_log_copy['assignedTo'] = call_log_copy['assignedTo'].astype(int)
call_log_copy.head()

# adjusting all the characters in status 
call_log_copy['status']= call_log_copy['status'].str.lower().str.capitalize()


#renaming the columns
call_log_copy.rename(columns={'callerID': 'caller_id', 
                         'agentID': 'agent_id', 
                         'complaintTopic':'complaint', 
                         'assignedTo': 'assigned_to', 
                         'resolutionDurationInHours':'resolution_duration_in_hours'}, 
                         inplace=True)

#change the first data in call_id to 1
call_details_copy['call_id'] = call_details_copy['call_id'].str.replace('ageentsGradeLevel','1')

# changing the datatype of call _id
call_details_copy['call_id'] = call_details_copy['call_id'].astype(int)

#saving the 2 cleaned datset to a csv file
cleaned_call_details = call_details_copy.to_csv('cleaned_call_details.csv', index=False)
cleaned_call_log = call_log_copy.to_csv('cleaned_call_log.csv', index=False)

print('successful')
