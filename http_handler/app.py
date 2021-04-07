import json

from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context()
def lambda_handler(event, context):

    # Simulate exception on "malicious" input
    if event["rawQueryString"] == "error=1":
        logger.error(event)
        raise Exception("Malicious input detected")

    return {"statusCode": 200, "body": json.dumps({"message": "hello world"})}
