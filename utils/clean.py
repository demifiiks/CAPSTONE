import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def copy_and_rename_columns(data, column_mapping):
    data_copy = data.copy()
    data_copy.rename(columns=column_mapping, inplace=True)
    return data_copy

def clean_call_details(call_details_copy):
    # Data cleaning steps for call_details
    call_details_copy['call_type'] = call_details_copy['call_type'].str.replace('-', '')
    call_details_copy['call_type'] = call_details_copy['call_type'].str.lower().str.capitalize()
    call_details_copy['call_type'] = call_details_copy['call_type'].str.strip()
    call_details_copy['call_id'] = call_details_copy['call_id'].str.replace('ageentsGradeLevel', '1')
    call_details_copy['call_id'] = call_details_copy['call_id'].astype(int)

def clean_call_log(call_log_copy):
    # Data cleaning steps for call_log
    call_log_copy['resolutionDurationInHours'] = call_log_copy['resolutionDurationInHours'].fillna(value=0)
    call_log_copy['assignedTo'] = call_log_copy['assignedTo'].fillna(call_log_copy['agentID'])
    call_log_copy['assignedTo'] = call_log_copy['assignedTo'].astype(int)
    call_log_copy['status'] = call_log_copy['status'].str.lower().str.capitalize()

def main():
    # Load the data
    call_details = load_data("call_details.csv")
    call_log = load_data("call_log.csv")

    # Define the column mapping for renaming
    call_details_column_mapping = {
        'callID': 'call_id',
        'callDurationInSeconds': 'duration_of_calls_in_sec',
        'agentsGradeLevel': 'agents_grade_level',
        'callType': 'call_type',
        'callEndedByAgent': 'call_ended_by_agent'
    }
    call_log_column_mapping = {
        'callerID': 'caller_id', 
        'agentID': 'agent_id', 
        'complaintTopic':'complaint', 
        'assignedTo': 'assigned_to', 
        'resolutionDurationInHours':'resolution_duration_in_hours'
    }

    # Copy and rename columns for call_details
    call_details_copy = copy_and_rename_columns(call_details, call_details_column_mapping)

    # Copy and rename columns for call_log
    call_log_copy = copy_and_rename_columns(call_log, call_log_column_mapping)

    # Data cleaning for call_details and call_log
    clean_call_details(call_details_copy)
    clean_call_log(call_log_copy)

    # Save the cleaned data to separate CSV files
    call_details_copy.to_csv('cleaned_call_details.csv', index=False)
    call_log_copy.to_csv('cleaned_call_log.csv', index=False)

if __name__ == "__main__":
    main()

transformed_dataset = main()
