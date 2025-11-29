#!/bin/bash

# ============================================================
# Script para destruir DynamoDB e SQS no LocalStack (SEM jq)
# Compatível com Windows (Git Bash) e Linux
# ============================================================

export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

LOCALSTACK_ENDPOINT="http://localhost:4566"

TABLE_NAME="AtivosTable"
QUEUE_NAME="fila-ativos"

echo "=============================================="
echo " Verificando LocalStack..."
echo "=============================================="

if ! curl -s $LOCALSTACK_ENDPOINT >/dev/null; then
    echo "❌ ERRO: LocalStack não está rodando."
    exit 1
else
    echo "✅ LocalStack ativo!"
fi

echo ""
echo "=============================================="
echo " Deletando tabela DynamoDB..."
echo "=============================================="

aws dynamodb delete-table \
  --table-name $TABLE_NAME \
  --endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null

if [ $? -eq 0 ]; then
    echo "🗑️ Tabela deletada: $TABLE_NAME"
else
    echo "ℹ️ Tabela já inexistente ou erro ignorável."
fi

echo ""
echo "=============================================="
echo " Buscando URL da fila SQS..."
echo "=============================================="

QUEUE_OUTPUT=$(aws sqs get-queue-url \
  --queue-name $QUEUE_NAME \
  --endpoint-url $LOCALSTACK_ENDPOINT 2>/dev/null)

# Extrai QueueUrl usando grep e sed — sem jq
QUEUE_URL=$(echo "$QUEUE_OUTPUT" | grep "QueueUrl" | sed 's/.*"QueueUrl": "\(.*\)".*/\1/')

if [ -n "$QUEUE_URL" ]; then
    echo "URL encontrada: $QUEUE_URL"

    aws sqs delete-queue \
      --queue-url "$QUEUE_URL" \
      --endpoint-url $LOCALSTACK_ENDPOINT &>/dev/null

    echo "🗑️ Fila deletada: $QUEUE_NAME"
else
    echo "ℹ️ A fila não existe."
fi

echo ""
echo "=============================================="
echo " Recursos restantes (verificação):"
echo "=============================================="

echo "📌 Tabelas DynamoDB:"
aws dynamodb list-tables --endpoint-url $LOCALSTACK_ENDPOINT

echo ""
echo "📌 Filas SQS:"
aws sqs list-queues --endpoint-url $LOCALSTACK_ENDPOINT

echo ""
echo "✨ Finalizado!"
