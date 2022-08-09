import json
import decimal
import os
import boto3
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Get the service resource
dynamodb = boto3.resource('dynamodb')

# Set environment variable
TABLE_NAME = os.environ('TABLE_NAME')


def handler(event, context):
    logger.info('incoming event: {}'.format(event))

    table = dynamodb.Table(TABLE_NAME)
    # Scan items in table
    try:
        response = table.scan()
    except ClientError as e:
        logger.info(e.response['Error']['Message'])
    else:
        # print item of the table
        for i in response['Items']:
            logger.info(json.dumps(i, cls=DecimalEncoder))

    return {
        'statusCode': 200,
        'body': 'success'
    }
