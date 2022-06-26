# Lambda Function to check the EC2 for a tag criteria

### Step : Create a policy to provide the necessary permissions to the lambda
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DeleteTags",
                "ec2:CreateTags",
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

### Step : Configure the following environment variables in lambda configuration
- EMAIL_ID : Email ID for mail
- EMAIL_PASSWORD : Password for mail auth

### Step : Configure the region in the lambda_function.py line:128


