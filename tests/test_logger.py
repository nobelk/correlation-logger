import boto3
import json
import logging
import pytest
import uuid
from moto import mock_aws, settings
from src.correlation_logger.logger import Logger, LogSink
from src.correlation_logger.cloudwatch_handler import CloudWatchHandler

TEST_REGION = "us-east-1"

"""
Returns a policy document in JSON format that are used for unit tests.
ARN is fake used for testing purposes.

"""
json_policy_doc = json.dumps(
    {
        "Version": "2024-12-17",
        "Statement": [
            {
                "Sid": "Route53LogsToCloudWatchLogs",
                "Effect": "Allow",
                "Principal": {"Service": ["route53.amazonaws.com"]},
                "Action": "logs:PutLogEvents",
                "Resource": "log_arn",
            }
        ],
    }
)

access_policy_doc = json.dumps(
    {
        "Version": "2024-12-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "logs.us-east-1.amazonaws.com"},
                "Action": "logs:PutSubscriptionFilter",
                "Resource": "destination_arn",
            }
        ],
    }
)


def test_console_logging():
    logger = Logger(name='default logger', log_level=logging.DEBUG)
    logger.debug('Debug log message', str(uuid.uuid4()))

def test_file_logging():
    logger_name = 'test-file-logger'
    logger = Logger(name=logger_name,
                    sink=LogSink.LOCAL_FILE,
                    log_level=logging.DEBUG,
                    log_file_name='test_log.log')
    correlation_id = str(uuid.uuid4())
    logger.debug('test message', correlation_id)
    with open('test_log.log') as log_file:
        content = log_file.read()
        assert content.find(f' DEBUG {logger_name} : {correlation_id}') != -1


@mock_aws
def test_cloudwatch_logging():
    conn = boto3.client("logs", TEST_REGION)
    log_group_name = "test-group"
    log_stream_name = "test-stream"
    log_handler = CloudWatchHandler(
        client=conn,
        log_group_name=log_group_name,
        log_stream_name=log_stream_name)
    logger = Logger(name='aws logger',
                    sink=LogSink.CLOUDWATCH,
                    log_level=logging.DEBUG,
                    handler=log_handler)
    logger.debug('Debug log message', str(uuid.uuid4()))
    res = conn.get_log_events(
        logGroupName=log_group_name, logStreamName=log_stream_name
    )
    events = res["events"]
    assert len(events) == 1
