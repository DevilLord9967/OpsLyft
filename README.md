# Lambda Function to check the EC2 for a tag criteria

### Step 1 : Create an IAM Role with the following JSON Policy to provide the necessary permissions to the lambda
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
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

### Step 2 : Create a Lambda function and choose the above IAM Role as its permissiona

### Step 3 : Configure the following environment variables in lambda configuration
- EMAIL_ID
- EMAIL_PASSWORD
- SMTP_HOST
- SMTP_PORT

### Step 4 : Configure the region in the lambda_function.py line:128

### Step 5 : Replace the code in the new lambda with the code in lambda_function.py

### Step 6 : Deploy the function

### Step 7 : Schedule the function

- Goto Add Trigger
- Select EventBridge
- Create a new role
- Add rule name like every-6hrs
- select rule type "Schedule expression"
- enter schedule expression value as "rate(6 hours)"
- Save

