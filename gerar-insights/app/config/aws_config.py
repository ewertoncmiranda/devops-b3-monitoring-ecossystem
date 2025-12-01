import boto3
import os
from botocore.config import Config

LOCALSTACK_ENDPOINT = os.getenv('LOCALSTACK_ENDPOINT', 'http://localstack:4566')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'tratar-ativos')
REGION = os.getenv('AWS_REGION', 'sa-east-1')

boto_config = Config(
    region_name=REGION,
    retries={'max_attempts': 5, 'mode': 'standard'},
    connect_timeout=5,
    read_timeout=30
)


sqs = boto3.client(
    'sqs',
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    config=boto_config
)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:4566",  # para LocalStack
    region_name="sa-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)


