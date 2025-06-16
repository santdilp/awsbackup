#!/usr/bin/env python3
# setup_database.py - Sets up the RDS database structure

import os
import pymysql
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ec2-user/aws-backup-demo/logs/setup_database.log'),
        logging.StreamHandler()
    ]
)

# Get environment variables
rds_endpoint = os.environ.get('RDS_ENDPOINT')
rds_password = os.environ.get('RDS_PASSWORD')

def get_db_connection():
    """Create a connection to the RDS database"""
    try:
        return pymysql.connect(
            host=rds_endpoint,
            user='admin',
            password=rds_password,
            charset='utf8mb4'
        )
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise

def setup_database():
    """Create database and tables"""
    logging.info("Setting up database structure...")
    
    # Retry logic for database connection
    max_retries = 5
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Create database
            logging.info("Creating demo database...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS demo")
            cursor.execute("USE demo")
            
            # Create documents table
            logging.info("Creating documents table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id VARCHAR(36) PRIMARY KEY,
                    title VARCHAR(255),
                    author VARCHAR(100),
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create metadata table
            logging.info("Creating metadata table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key_name VARCHAR(50) PRIMARY KEY,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Insert initial metadata
            cursor.execute("""
                INSERT INTO metadata (key_name, value) VALUES 
                ('backup_demo_version', '1.0'),
                ('created_date', NOW())
                ON DUPLICATE KEY UPDATE value=VALUES(value)
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.info("Database setup completed successfully!")
            return
            
        except Exception as e:
            logging.warning(f"Database setup attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Maximum retries reached. Database setup failed.")
                raise

if __name__ == "__main__":
    try:
        setup_database()
    except Exception as e:
        logging.error(f"Error in database setup: {e}")
        exit(1)