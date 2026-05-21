Gerar Insights - Motor Financeiro

Aplicacao Python responsavel por ser o cerebro analitico do ecossistema. Operando como um worker assincrono em loop infinito, consome snapshots de ativos brutos de uma fila SQS, aplica matematica financeira e grava historicos e insights em MySQL.

RESPONSABILIDADES PRINCIPAIS

1. Consumo Robusto (SQS) - Le mensagens da fila sem gargalos, processa e apaga de forma eficiente.
2. Historico Bruto - Armazena snapshots de mercado diarios dos ativos na tabela historico_acoes.
3. Calculo de Insights - Aplica calculos financeiros (Preco Justo Benjamin Graham, Margem de Seguranca) e emite recomendacoes (COMPRA/VENDA/NEUTRO).

TECNOLOGIAS

- boto3: SDK AWS para acesso a SQS e DynamoDB
- SQLAlchemy + PyMySQL: Gerenciamento de conexoes e persistencia em MySQL
- python-dotenv: Carregamento de variaveis de ambiente via arquivo .env
- python-json-logger: Logs estruturados

CONFIGURACAO CENTRALIZADA

Todas as configuracoes estao centralizadas em app/config/settings.py seguindo principios SOLID e clean code:
- Leitura de variaveis de ambiente com defaults seguros
- Validacao de variaveis obrigatorias
- Logging de configuracao na inicializacao

VARIAVEIS DE AMBIENTE

Defaults para docker: localstack:4566, mysql:3306
Para execucao local: defina variaveis apontando para localhost

AWS/LocalStack:
- LOCALSTACK_ENDPOINT (default: http://localstack:4566)
  Local: http://localhost:4566
- QUEUE_NAME (default: tratar-ativos)
- AWS_REGION (default: sa-east-1)
- AWS_ACCESS_KEY_ID (default: test)
- AWS_SECRET_ACCESS_KEY (default: test)

DynamoDB:
- DYNAMO_ENDPOINT (default: http://localstack:4566)
  Local: http://localhost:4566
- DYNAMO_TABLE_NAME (default: insights-refinados)

Banco de Dados:
- DB_DRIVER (default: mysql+pymysql)
- DB_HOST (default: mysql)
  Local: localhost
- DB_PORT (default: 3306)
  Local: 3305
- DB_USER (default: spring)
- DB_PASS (default: spring123)
- DB_NAME (default: minha_base)

Retry/Timeout:
- RETRY_ATTEMPTS (default: 3)
- RETRY_DELAY (default: 10 segundos)

QUICK START - EXECUCAO LOCAL

Prerequisitos: LocalStack e MySQL rodando em localhost

1. Criar ambiente virtual:
   python -m venv venv
   .\venv\Scripts\Activate.ps1  (Windows)
   source venv/bin/activate      (Linux/Mac)

2. Instalar dependencias:
   pip install -r requirements.txt

3. Criar arquivo .env.local com configuracoes para localhost:
   DB_HOST=localhost
   DB_PORT=3305
   LOCALSTACK_ENDPOINT=http://localhost:4566
   DYNAMO_ENDPOINT=http://localhost:4566

4. Executar:
   python main.py

EXECUCAO VIA DOCKER

Na raiz do projeto:
   docker-compose up --build -d gerar-insights

O container automaticamente usa rede interna docker (localstack:4566, mysql:3306).

ESTRUTURA DO PROJETO

gerar-insights/
  app/
    config/
      settings.py              Configuracoes centralizadas (SOLID)
      aws_config.py            Clientes boto3 (SQS, DynamoDB)
      database_config.py       SqlAlchemy engine
      config_logger.py         Setup de logs
    core/
      - Logica de indicadores e insights
    entrypoint/
      entrypoint_sqs.py        Consumer SQS
    external/
      - Integracao com servicos externos
  main.py                       Ponto de entrada
  requirements.txt              Dependencias
  Dockerfile                    Imagem Docker

TESTES

Execute testes automatizados:
   pytest tests/ -v

NOTAS IMPORTANTES

- Arquivo .env.local nao deve ser commitado (.gitignore ja ignora)
- Senhas/tokens nao devem ser hard-coded em producao
- Use secrets manager (AWS Secrets Manager, Vault) em producao
- Verifique logs iniciais para confirmar que configuracao foi carregada

