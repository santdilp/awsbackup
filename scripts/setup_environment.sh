#!/bin/bash
# setup_environment.sh - Sets up environment variables and directories

echo "Setting up AWS Backup Demo environment..."

# Create necessary directories
mkdir -p /home/ec2-user/aws-backup-demo/data
mkdir -p /home/ec2-user/aws-backup-demo/logs

# Set permissions
chmod 755 /home/ec2-user/aws-backup-demo/scripts/*.sh
chmod 755 /home/ec2-user/aws-backup-demo/scripts/*.py

# Create environment file
cat > /home/ec2-user/aws-backup-demo/.env << EOF
S3_BUCKET_NAME=$S3_BUCKET_NAME
DYNAMODB_TABLE_NAME=$DYNAMODB_TABLE_NAME
RDS_ENDPOINT=$RDS_ENDPOINT
RDS_PASSWORD=$RDS_PASSWORD
EOF

echo "Environment setup complete!"