import boto3
from configparser import ConfigParser
import psycopg2 
import pandas as pd
# import redshift_connector


region = 'ap-southeast-1'
bucket_name = 'weserves'

config = ConfigParser()
config.read('.env')

access_key = config['AWS']['access_key']
secret_key =  config['AWS']['secret_key']

ACCESS_KEY = config['AWS']['access_key']
SECRET_KEY = config['AWS']['secret_key']
BUCKET_NAME = config['AWS']['bucket_name']
REGION = config['AWS']['region']

# DWH_ROLE = config['DWH']['DWH_ROLE']
# DWH_USERNAME = config['DWH']['DWH_USERNAME']
# DWH_PASSWEORD = config['DWH']['DWH_PASSWORD']
# DWH_HOST = config['DWH']['DWH_HOST']
# DWH_DATABASE = config['DWH']['DWH_DATABASE']



# RAW_SCHEMA = config['DWH']['raw_data_schema']
DEV_SCHEMA = config['DWH']['dev_schema']


s3_lake_path = "s3://{}/{}.csv"


def create_s3_bucket():
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION
        )
        client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint': REGION
            }
        )
        print('Bucket Created in S3lake')
    except Exception as error:
        print('Creation failed or Bucket exists')


def connect_to_warehouse():
    conn = redshift_connector.connect(
        host=DWH_HOST, user=DWH_USER, password=DWH_PASSWEORD, database=DWH_DB
    )
    print('Connected to DWH')
    return conn
