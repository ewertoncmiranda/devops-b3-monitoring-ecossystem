#!/bin/bash
set -e

awslocal sqs create-queue \
  --queue-name tratar-ativos \
  --attributes VisibilityTimeout=30 \
  --region sa-east-1

echo "Fila 'tratar-ativos' criada com sucesso!"
