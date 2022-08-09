#!/usr/bin/env python3
import os

import aws_cdk as cdk

from dynamodb_lambda.dynamodb_lambda_stack import DynamodbLambdaStack


app = cdk.App()
DynamodbLambdaStack(app, "DynamodbLambdaStack")

app.synth()
