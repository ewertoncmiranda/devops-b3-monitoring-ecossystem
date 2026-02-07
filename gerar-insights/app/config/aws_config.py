import boto3
import os
from botocore.config import Config
from app.config.config_logger import setup_logger

logger = setup_logger()

# =====================
# AWS/LocalStack Configuration
# =====================
LOCALSTACK_ENDPOINT = os.getenv('LOCALSTACK_ENDPOINT', 'http://localhost:4566')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'tratar-ativos')
REGION = os.getenv('AWS_REGION', 'sa-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'test')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'test')

logger.info(f"Configuring AWS with endpoint: {LOCALSTACK_ENDPOINT}")
logger.info(f"SQS Queue: {QUEUE_NAME}")

boto_config = Config(
    region_name=REGION,
    retries={'max_attempts': 5, 'mode': 'standard'},
    connect_timeout=5,
    read_timeout=30
)

# =====================
# SQS Client
# =====================
sqs = boto3.client(
    'sqs',
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION,
    config=boto_config
)

# =====================
# DynamoDB Client (if needed)
# =====================
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

logger.info("AWS configuration completed")

