#!/bin/bash
# install_dependencies.sh - Installs required packages and libraries

echo "Installing dependencies..."

# Update system packages
yum update -y

# Install system packages
yum install -y python3 python3-pip mysql git jq

# Install Python packages
pip3 install boto3 pymysql faker

echo "Dependencies installation complete!"