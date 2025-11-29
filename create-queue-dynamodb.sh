#!/bin/bash

# ============================================================
# Script para criar DynamoDB e SQS no LocalStack
# Compatível com Windows (Git Bash) e Linux
# ============================================================

export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

LOCALSTACK_ENDPOINT="http://localhost:4566"

echo "=============================================="
echo " Verificando se LocalStack está respondendo..."
echo "=============================================="

if ! curl -s $LOCALSTACK_ENDPOINT >/dev/null; then
    echo "❌ ERRO: LocalStack não está rodando em $LOCALSTACK_ENDPOINT"
    echo "Inicie com:  localstack start  ou via docker-compose"
    exit 1
else
    echo "✅ LocalStack está ativo!"
fi

echo ""
echo "=============================================="
echo " Criando tabela DynamoDB..."
echo "=============================================="

TABLE_NAME="AtivosTable"

aws dynamodb create-table \
  --table-name $TABLE_NAME \
  --attribute-definitions AttributeName=pk,AttributeType=S \
  --key-schema AttributeName=pk,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null

if [ $? -eq 0 ]; then
  echo "✅ Tabela criada: $TABLE_NAME"
else
  echo "ℹ️ Tabela já existe ou ocorreu outro aviso."
fi

echo ""
echo "=============================================="
echo " Criando fila SQS..."
echo "=============================================="

QUEUE_NAME="fila-ativos"

aws sqs create-queue \
  --queue-name $QUEUE_NAME \
  --attributes VisibilityTimeout=30 \
  --endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null

if [ $? -eq 0 ]; then
  echo "✅ Fila criada: $QUEUE_NAME"
else
  echo "ℹ️ A fila já existe ou ocorreu outro aviso."
fi

echo ""
echo "=============================================="
echo " Listando recursos criados:"
echo "=============================================="

echo "📌 Tabelas DynamoDB:"
aws dynamodb list-tables --endpoint-url $LOCALSTACK_ENDPOINT

echo ""
echo "📌 Filas SQS:"
aws sqs list-queues --endpoint-url $LOCALSTACK_ENDPOINT

echo ""
echo "✨ Finalizado!"
