from curses.ascii import TAB
import json
import decimal
import uuid
import os
import boto3


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
  # put item in table
  response = table.put_item(
    Item={
      'id': str(uuid.uuid4())
    }
  )

  print('Successfully put item')
  print(json.dumps(response, indent=4, cls=DecimalEncoder))

  return {
    'statusCode': 200,
    'body': 'success'
  }