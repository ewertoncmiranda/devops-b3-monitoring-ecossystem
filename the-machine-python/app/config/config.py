# app/config.py
import os
from botocore.config import Config

LOCALSTACK_ENDPOINT = os.getenv('LOCALSTACK_ENDPOINT', 'http://localstack:4566')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'themachine')
REGION = os.getenv('AWS_REGION', 'sa-east-1')

boto_config = Config(
    region_name=REGION,
    retries={'max_attempts': 5, 'mode': 'standard'},
    connect_timeout=5,
    read_timeout=30
)

