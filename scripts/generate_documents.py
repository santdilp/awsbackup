#!/usr/bin/env python3
# generate_documents.py - Generates sample documents and stores them in S3, DynamoDB, and RDS

import boto3
import pymysql
import json
import uuid
import time
import os
import logging
from faker import Faker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ec2-user/aws-backup-demo/logs/generate_documents.log'),
        logging.StreamHandler()
    ]
)

# Initialize Faker
fake = Faker()

# Get environment variables
s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
dynamodb_table_name = os.environ.get('DYNAMODB_TABLE_NAME')
rds_endpoint = os.environ.get('RDS_ENDPOINT')
rds