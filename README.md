# Using Amazon Managed Service for Grafana to Troubleshoot a Serverless Application

To build and deploy the application for the first time, run the following in your shell:

```bash
sam build -p -u
sam deploy --guided
```

The first command will build the Lambda functions in parallel using a container. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region. We will use `amg-blog` throughout this sample.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

### Generate API traffic

We need to generate some metrics and logs to use as part of our troubleshooting exercise.

This step will generate traffic to the API Gateway endpoint, which will invoke the `HttpHandlerFunction` Lambda function repeatedly for 15 minutes. The code will randomly inject errors into the HTTP requests, which can be found by correllating the function metrics and logs.
Find the `GenerateTrafficFunction` name from the `sam deploy` output. It will be of the form `amg-blog-GenerateTrafficFunction-1234567ABCDEF`.

Invoke the Lambda function using the AWS CLI:

```bash
aws lambda invoke --function-name <your-function-name> --invocation-type Event /dev/null
```

Replace `<your-function-name>` above with the name of the Lambda function from the `sam deploy` output.

We use an asynchronous (event-based) invocation here because we don't retrieve a return value, and send the output to `/dev/null` because we don't need to work with it in a file.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name amg-blog
```

