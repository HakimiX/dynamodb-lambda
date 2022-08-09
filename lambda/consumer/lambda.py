from __future__ import print_function
from curses.ascii import TAB

import json
import decimal
from msilib import Table
from multiprocessing.connection import Client
import os
import boto3
from botocore.exceptions import ClientError

from lambda .producer.lambda import TABLE_NAME


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
  table = dynamodb.Table(TABLE_NAME)
  # Scan items in table
  try:
    response = table.scan()
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    # print item of the table 
    for i in response['Items']:
      print(json.dumps(i, cls=DecimalEncoder))
  
  return {
    'statusCode': 200,
    'body': 'success'
  }