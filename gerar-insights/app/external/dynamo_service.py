import logging

import boto3
import os
from boto3.dynamodb.types import TypeSerializer
from decimal import Decimal

serializer = TypeSerializer()

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

def to_dynamo_safe(value):
    if isinstance(value, float):
        return Decimal(str(value))
    elif isinstance(value, dict):
        return {k: to_dynamo_safe(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [to_dynamo_safe(v) for v in value]
    return value

def salvar_insights_em_dynamodb(ativo, insights):
    endpoint = os.getenv('DYNAMO_ENDPOINT', 'http://localstack:4566')
    region = os.getenv('AWS_REGION', 'sa-east-1')
    access_key = os.getenv('AWS_ACCESS_KEY_ID', 'test')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
    table_name = os.getenv('DYNAMO_TABLE_NAME', 'insights-refinados')

    dynamodb = boto3.client(
        'dynamodb',
        endpoint_url=endpoint,
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    symbol = ativo.get("symbol")
    regular_time = ativo.get("regularMarketTime") or "no-time"

    if not symbol:
        raise ValueError("O campo 'symbol' é obrigatório e está ausente ou nulo.")

    item = {
        "symbol": {"S": symbol},
        "insights_id": {"S": f"{symbol}#{regular_time}"}
    }

    safe_insights = to_dynamo_safe(insights)
    for k, v in safe_insights.items():
        item[k] = serializer.serialize(v)

    dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    log.info(f"✔️ Insight do ativo {ativo} salvo na tabela {table_name}: Insight -> :{insights}")