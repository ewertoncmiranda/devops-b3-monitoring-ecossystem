#!/bin/bash

# ============================================================
# Script para criar DynamoDB e SQS no LocalStack
# Compatível com Windows (Git Bash) e Linux
# ============================================================

export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_REGION="sa-east-1"
export AWS_DEFAULT_REGION="sa-east-1"

LOCALSTACK_ENDPOINT="http://localhost:4566"

echo "=============================================="
echo " Verificando se LocalStack está respondendo..."
echo "=============================================="

if ! curl -s $LOCALSTACK_ENDPOINT >/dev/null; then
    echo "ERRO: LocalStack não está rodando em $LOCALSTACK_ENDPOINT"
    echo "Inicie com:  localstack start  ou via docker-compose"
    exit 1
else
    echo "LocalStack está ativo!"
fi


echo ""
echo "=============================================="
echo " Criando fila SQS..."
echo "=============================================="

QUEUE_NAME="fila-ativos"
QUEUE_NAME_INSIGHTS="gerar-insights"
QUEUE_NAME_TRATAR_ATIVOS="tratar-ativos"

awslocal sqs create-queue \
  --queue-name $QUEUE_NAME \
  --attributes VisibilityTimeout=30 \
  --endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null


awslocal sqs create-queue \
  --queue-name $QUEUE_NAME_INSIGHTS \
  --attributes VisibilityTimeout=30 \
  --endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null


awslocal sqs create-queue \
--queue-name $QUEUE_NAME_TRATAR_ATIVOS \
--attributes VisibilityTimeout=30 \
--endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null


if [ $? -eq 0 ]; then
  echo "Fila criada: $QUEUE_NAME_INSIGHTS"
else
  echo "A fila $QUEUE_NAME_INSIGHTS já existe ou ocorreu outro aviso."
fi

if [ $? -eq 0 ]; then
  echo "Fila criada: $QUEUE_NAME_TRATAR_ATIVOS"
else
  echo "A fila $QUEUE_NAME_TRATAR_ATIVOS já existe ou ocorreu outro aviso."
fi

if [ $? -eq 0 ]; then
  echo "Fila criada: $QUEUE_NAME"
else
  echo "A fila $QUEUE_NAME já existe ou ocorreu outro aviso."
fi

echo ""
echo "=============================================="
echo " Listando recursos criados:"
echo "=============================================="

echo "Tabelas DynamoDB:"
aws dynamodb list-tables --endpoint-url $LOCALSTACK_ENDPOINT

echo ""
echo "Filas SQS:"
aws sqs list-queues --endpoint-url $LOCALSTACK_ENDPOINT

echo ""
echo "Finalizado!"
