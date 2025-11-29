import os
import boto3
import logging
from botocore.config import Config
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

LOCALSTACK_ENDPOINT = os.getenv('LOCALSTACK_ENDPOINT', 'http://localstack:4566')
REGION = os.getenv('REGION', 'sa-east-1')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'tratar-ativos')
QUEUE_NAME_INSIGHTS = os.getenv('QUEUE_NAME_INSIGHTS', 'tratar-insights')
DYNAMODB_NAME = os.getenv('DYNAMODB_NAME', 'insights-refinados')
SECRET_NAME = os.getenv('AWS_SECRET_NAME', 'minha-secret')
SECRET_VALUE = os.getenv('AWS_SECRET_VALUE', 'kJfyqy8yUVj94SivLsKq4Q')



def get_boto3_client(service: str) -> boto3.client:
    return boto3.client(
        service,
        region_name=REGION,
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        config=Config(
            region_name=REGION,
            retries={'max_attempts': 5, 'mode': 'standard'},
            connect_timeout=5,
            read_timeout=30
        )
    )

sqs_client = get_boto3_client('sqs')
dynamo_client = get_boto3_client('dynamodb')
secrets_client = get_boto3_client('secretsmanager')


def ensure_queue(queue_name: str) -> str:
    try:
        url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        log.info(f"✔️ Fila já existente: {queue_name}")
        return url
    except ClientError as e:
        if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
            log.warning(f"⚠️ Fila '{queue_name}' não encontrada. Criando...")
            response = sqs_client.create_queue(QueueName=queue_name)
            log.info(f"✅ Fila criada: {response['QueueUrl']}")
            return response['QueueUrl']
        log.error(f"❌ Erro ao verificar/criar fila: {e}")
        raise


def ensure_dynamodb_table(table_name: str) -> dict:
    try:
        response = dynamo_client.describe_table(TableName=table_name)
        log.info(f"✔️ Tabela já existente: {table_name}")
        return response['Table']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            log.warning(f"⚠️ Tabela '{table_name}' não encontrada. Criando...")

            response = dynamo_client.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'symbol', 'KeyType': 'HASH'},         # Partition key
                    {'AttributeName': 'insights_id', 'KeyType': 'RANGE'}    # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'symbol', 'AttributeType': 'S'},
                    {'AttributeName': 'insights_id', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            log.info(f"✅ Tabela criada: {table_name}")
            return response
        log.error(f"❌ Erro ao verificar/criar tabela: {e}")
        raise
