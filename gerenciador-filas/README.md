# Gerenciador de Filas

Este é um script utilitário focado em **infraestrutura e resiliência**. Ele tem o objetivo de substituir scripts Shell tradicionais para provisionar e garantir que as filas do AWS SQS (LocalStack) existam antes que as aplicações consumidoras tentem se conectar.

## Responsabilidades
- Conectar-se ao LocalStack.
- Criar a fila alvo (ex: `tratar-ativos`) de forma idempotente.
- Aplicar *retry backoff* caso o LocalStack ainda não esteja pronto no momento do boot do container.

## Libs Principais
- **boto3**: SDK oficial da AWS para interagir com o SQS.

## Variáveis de Ambiente e Configuração
A aplicação tem suporte dinâmico a execução local vs docker via variável `ENVIRONMENT`.

| Variável | Padrão (Local) | Descrição |
| --- | --- | --- |
| `ENVIRONMENT` | `local` | Se `docker`, o script apontará nativamente para o container `http://localstack:4566`. |
| `LOCALSTACK_ENDPOINT` | `http://localhost:4566` | Ponto de acesso do SQS (sobrescrito no Docker). |
| `QUEUE_NAME` | `tratar-ativos` | Nome da fila que será criada. |
| `AWS_REGION` | `sa-east-1` | Região simulada. |

## Como Rodar

**Local (Via IDE / Terminal):**
Crie um `.env` caso queira sobrescrever, crie seu venv e instale os pacotes:
```bash
pip install -r requirements.txt
python main.py
```

**Docker:**
Executado automaticamente pelo `docker-compose.yml` usando o build context do diretório.
