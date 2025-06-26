import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def get_boto3_client(service: str, region: str, endpoint: str) -> boto3.client:
    return boto3.client(
        service,
        region_name=region,
        endpoint_url=endpoint,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        config=Config(
            region_name=region,
            retries={'max_attempts': 5, 'mode': 'standard'},
            connect_timeout=5,
            read_timeout=30
        )
    )


# Configurações
LOCALSTACK_ENDPOINT = os.getenv('LOCALSTACK_ENDPOINT', 'http://localstack:4566')
REGION = os.getenv('AWS_REGION', 'sa-east-1')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'themachine')
DYNAMODB_NAME = os.getenv('DYNAMODB_NAME', 'themachine-db')

# Clientes AWS simulados via LocalStack
sqs_client = get_boto3_client('sqs', REGION, LOCALSTACK_ENDPOINT)
dynamo_client = get_boto3_client('dynamodb', REGION, LOCALSTACK_ENDPOINT)


def ensure_queue(queue_name: str) -> str:
    try:
        url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        print(f"✔️ Fila '{queue_name}' já existe.")
        return url
    except ClientError as e:
        if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
            print(f"⚠️ Fila '{queue_name}' não encontrada. Criando nova...")
            response = sqs_client.create_queue(QueueName=queue_name)
            return response['QueueUrl']
        raise


def ensure_dynamodb_table(table_name: str) -> dict:
    try:
        response = dynamo_client.describe_table(TableName=table_name)
        print(f"✔️ Tabela '{table_name}' já existe.")
        return response['Table']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"⚠️ Tabela '{table_name}' não encontrada. Criando nova...")
            return dynamo_client.create_table(
                TableName=table_name,
                KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
        raise
