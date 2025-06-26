
import boto3
from app.config.config import boto_config
from app.config.config import LOCALSTACK_ENDPOINT


sqs = boto3.client(
    'sqs',
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    config=boto_config
)
