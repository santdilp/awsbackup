# Demo Overview

This environment creates:

1. Complete VPC with public and private subnets
2. RDS MySQL database for structured data storage
3. DynamoDB table for NoSQL data
4. S3 bucket for object storage
5. EC2 instance that generates sample data across all services
6. AWS Backup configuration with:
   - Tag-based resource selection
   - Daily and weekly backup plans
   - Lifecycle management
   - Cross-region backup copies
   - Delegated administrator validation

All resources are tagged with BackupDemo=true to demonstrate tag-based backup selection.

## Deployment Instructions

### Prerequisites

- AWS CLI configured with appropriate permissions
- An AWS account with access to all required services
- If using delegated administrator features, AWS Organizations must be set up

### Deployment Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/santdilp/awsbackup.git
   cd awsbackup
   ```

2. Upload the nested templates to an S3 bucket:
   
   ```bash
   # Create an S3 bucket (replace BUCKET_NAME with your unique bucket name)
   aws s3 mb s3://BUCKET_NAME
   
   # Upload the CloudFormation templates
   aws s3 cp cloudformation/ s3://BUCKET_NAME/cloudformation/ --recursive
   ```

3. Deploy the CloudFormation stack:
   
   ```bash
   aws cloudformation create-stack \
     --stack-name aws-backup-demo \
     --template-body file://cloudformation/main.yaml \
     --parameters \
     ParameterKey=TemplateBucketName,ParameterValue=BUCKET_NAME \
     ParameterKey=DelegatedAdminAccountId,ParameterValue=ACCOUNT_ID \
     --capabilities CAPABILITY_IAM
   ```

4. Monitor the deployment:
   ```bash
   aws cloudformation describe-stacks --stack-name aws-backup-demo
   ```

## Demo Walkthrough

After deployment completes:

1. Access the EC2 instance using AWS Systems Manager Session Manager
2. Verify data generation by checking:
   - S3 bucket contents
   - DynamoDB table items
   - RDS database records

3. Explore AWS Backup console to see:
   - Resources protected by the backup plan
   - Backup vault contents
   - Scheduled backup jobs

4. Test restore operations for different resource types

## Centralized Backup Management

This demo includes validation for AWS Organizations delegated administrator setup:

- The CloudFormation template validates if the specified account is properly registered as a delegated administrator for AWS Backup
- If using the same account (no delegated admin), this validation is skipped

## Security Improvements

This demo implements several security best practices:

- Uses AWS Systems Manager Session Manager for EC2 access instead of SSH keys
- No inbound SSH ports are open in security groups when using SSM
- Auto-generates secure database passwords using AWS Secrets Manager
- Stores credentials securely and provides access only to resources that need them

## Cleanup

To avoid ongoing charges, delete the CloudFormation stack when finished:

```bash
aws cloudformation delete-stack --stack-name aws-backup-demo
```

## Additional Resources

- [AWS Backup Documentation](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html)
- [AWS Organizations and AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/manage-cross-account.html)
- [AWS Backup Best Practices](https://aws.amazon.com/blogs/storage/best-practices-for-aws-backup/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.