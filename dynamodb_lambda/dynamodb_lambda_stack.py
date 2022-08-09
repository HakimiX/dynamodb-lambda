from math import prod
from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as event_targets,
    Stack,
    Duration
)
from constructs import Construct

class DynamodbLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table 
        demo_table = dynamodb.Table(
            self, 'demo_table',
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Producer Lambda 
        producer_lambda = _lambda.Function(
            self, 'producer_lambda_function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='lambda.handler',
            code=_lambda.Code.from_asset('./lambda/producer')
        )

        # Environment variables
        producer_lambda.add_environment('TABLE_NAME', demo_table.table_name)

        # Grant producer lambda permission to write to dynamodb (demo_table)
        demo_table.grant_write_data(producer_lambda)

        # Consumer Lambda 
        consumer_lambda = _lambda.Function(
            self, 'consumer_lambda_function',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='lambda.handler',
            code=_lambda.Code.from_asset('./lambda/consumer')
        )

        # Environment variables 
        consumer_lambda.add_environment('TABLE_NAME', demo_table.table_name)

        # Grant consumer lambda permission to read from dynamodb (demo_table)
        demo_table.grant_read_data(consumer_lambda)

        # CloudWatch event rule 
        one_minute_rule = events.Rule(
            self, 'one_minute_rule',
            schedule=events.Schedule.rate(Duration.minutes(1))
        )

        # Add targets to CloudWatch events
        one_minute_rule.add_target(event_targets.LambdaFunction(producer_lambda))
        one_minute_rule.add_target(event_targets.LambdaFunction(consumer_lambda))

