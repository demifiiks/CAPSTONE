import pandas as pd
import os 
from configparser import ConfigParser
from utils.helper import create_s3_bucket, connect_to_warehouse, DEV_SCHEMA, RAW_SCHEMA, s3_lake_path, BUCKET_NAME
from utils.clean import main
from sql_statements.create import schema, raw_data_schema, transformed_kpi
from sql_statements.transform import insert_into_transformed_kpi
from utils.constants import kpi_tables

config = ConfigParser()
config.read('.env')

region = config['AWS']['region']
bucket_name = config['AWS']['bucket_name']

access_key = config['AWS']['access_key']
secret_key =  config['AWS']['secret_key']
 
host = config['DB_CRED']['host']
username = config['DB_CRED']['username']
password = config['DB_CRED']['password']
database = config['DB_CRED']['database']
 
DWH_HOST = config['DWH']['DWH_HOST']
DWH_USER = config['DWH']['DWH_USER']
DWH_DB = config['DWH']['DWH_DB']
DWH_PASSWEORD = config['DWH']['DWH_PASSWORD']

# dwh_host = config['DWH']['dwh_host']
# dwh_username = config['DWH']['dwh_username']
# dwh_password = config['DWH']['dwh_password']
# dwh_database = config['DWH']['dwh_database']
# role =config['DWH']['role']

# Create the RAW and DEV schemas
def create_raw_schema():
    conn = connect_to_warehouse()
    cursor = conn.cursor()
    print('Create raw schema')
    cursor.execute(schema.format(RAW_SCHEMA))
    conn.commit()
    cursor.close()

def create_dev_schema():
    conn = connect_to_warehouse()
    cursor = conn.cursor()
    print('Create dev schema')
    cursor.execute(transformed_kpi.format(DEV_SCHEMA))
    conn.commit()
    cursor.close()

# Create schema  and TRANSFORMED tables
def create_raw_tables():
    conn = connect_to_warehouse()
    cursor = conn.cursor()
    for query in raw_data_schema:
        print(f"{query[:35]}")
        cursor.execute(query.format(RAW_SCHEMA))
        conn.commit()
    print('All RAW tables created')
    cursor.close()

def create_transformed_tables():
    conn = connect_to_warehouse()
    cursor = conn.cursor()
    for query in kpi_tables:
        print(f"{query[:45]}")
        cursor.execute(query.format(DEV_SCHEMA))
        conn.commit()
    print('All TRANSFORMED tables created')
    cursor.close()

# Copy data from S3 to DWH
def copy_from_s3_dwh():
    try:
        dwh_conn = connect_to_warehouse()
        cursor = dwh_conn.cursor()
        for table in kpi_tables:
            print(f"Copying {table} from S3 to DWH")
            table_copy_query = f"""
            copy {RAW_SCHEMA}.{table}
            from '{s3_lake_path.format(BUCKET_NAME, table)}'
            iam_role '{DWH_ROLE}' # Configure your DWH
            delimiter ','
            ignoreheader 1;
        """
            cursor.execute(table_copy_query)
            dwh_conn.commit()
        cursor.close()
        dwh_conn.close()
    except Exception as e:
        print(e)

# Insert data into TRANSFORMED tables
def insert_into_trans_tables():
    conn = connect_to_warehouse()
    cursor = conn.cursor()
    for query in insert_into_transformed_kpi:
        print(f"{query[:20]}")
        cursor.execute(query.format(DEV_SCHEMA))
        conn.commit()
    print('All TRANSFORMED tables inserted')
    cursor.close()

# Extract and process data using your `main` function
def extract_all_jobs():
    for job in main:
        job()

if __name__ == "__main__":
    create_raw_schema()
    create_dev_schema()
    create_raw_tables()
    create_transformed_tables()
    copy_from_s3_dwh()
    insert_into_trans_tables()
    extract_all_jobs()
