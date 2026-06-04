# B3 Monitoring & AI Insights Ecosystem 

-----
Projeto modular para captura, processamento e armazenamento de insights sobre ativos (B3). Composto por:
- `gestor-ativos-brutos` — Serviço Java (Spring Boot) que processa e publica/consome mensagens (SQS), expõe métricas e healthchecks.
- `gerar-insights` — Worker Python que consome filas, realiza análise e persiste dados no banco.
- Infra local via Docker Compose: MySQL, LocalStack (SQS), Terraform provisioner.

Este README reúne instruções de execução local, interoperabilidade entre componentes e as variáveis de ambiente OBRIGATÓRIAS que, se ausentes, causam falha na aplicação.

Proposta de valor técnico
-----------------------------------------------------------
- Demonstra arquitetura orientada a eventos (SQS), integração entre serviços Java e Python.
- Mostra habilidades em Docker, Docker Compose, LocalStack, Terraform, Spring Boot, Python e testes.
- Mostra práticas operacionais: healthchecks, actuator, métricas, e separação de responsabilidades.

# EXECUTE O ECOSSISTEMA LOCALMENTE COM DOCKER-COMPOSE COM AS IMAGENS CONSOLIDADAS NO DOCKER HUB
````json
services:

  localstack:
    image: localstack/localstack:3.3
    container_name: localstack
    environment:
      - SERVICES=sqs
      - EDGE_PORT=4566
      - AWS_DEFAULT_REGION=sa-east-1
      - DEBUG=1
    ports:
      - "4566:4566"
    volumes:
      - localstack_data:/var/lib/localstack

    healthcheck:
      test: [ "CMD", "awslocal", "sqs", "list-queues" ]
      interval: 5s
      timeout: 3s
      retries: 30

  terraform-provisioner:
    image: hashicorp/terraform:latest
    container_name: terraform-provisioner
    volumes:
      - ./infra:/infra
    working_dir: /infra
    environment:
      - AWS_ACCESS_KEY_ID=test
      - AWS_SECRET_ACCESS_KEY=test
      - AWS_DEFAULT_REGION=sa-east-1
      - TF_VAR_aws_endpoint=http://localstack:4566
    entrypoint: /bin/sh -c "terraform init && terraform apply -auto-approve"
    depends_on:
      localstack:
        condition: service_healthy

  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: minha_base
      MYSQL_USER: spring
      MYSQL_PASSWORD: spring123
    ports:
      - "3305:3306"
    command: --default-authentication-plugin=mysql_native_password
    healthcheck:
      test: [ "CMD", "mysqladmin", "ping", "-h", "localhost" ]
      interval: 5s
      timeout: 3s
      retries: 15
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql-init:/docker-entrypoint-initdb.d

  gestor-ativos-brutos:
    image: ewertonmiranda/gestor-ativos-brutos:latest

    container_name: gestor-ativos-brutos

    restart: always

    depends_on:
      mysql:
        condition: service_started
      localstack:
        condition: service_healthy
      terraform-provisioner:
        condition: service_completed_successfully

    ports:
      - "8091:8091"

    environment:
      SPRING_PROFILES_ACTIVE: dev
      SERVER_PORT: 8091

      AWS_REGION: sa-east-1
      AWS_ACCESS_KEY_ID: test
      AWS_SECRET_ACCESS_KEY: test
      AWS_SQS_ENDPOINT_BASE: http://localstack:4566
      AWS_SQS_QUEUE_URL: http://localstack:4566/000000000000/tratar-ativos
      BRAPI_API_KEY: ${BRAPI_API_KEY}
      GEMINI_API_KEY: ${GEMINI_API_KEY}

    volumes:
      - ./logs/java:/var/log/myapp

  gerar-insights:
    image: ewertonmiranda/gerar-insights:latest
    container_name: gerar-insights
    ports:
      - "8080:8080"
    depends_on:
      mysql:
        condition: service_healthy
      localstack:
        condition: service_healthy
      terraform-provisioner:
        condition: service_completed_successfully
    environment:
      ENVIRONMENT: docker
      DB_USER: spring
      DB_PASS: spring123
      DB_NAME: minha_base
      LOCALSTACK_ENDPOINT: http://localstack:4566
      AWS_REGION: sa-east-1
      AWS_ACCESS_KEY_ID: test
      AWS_SECRET_ACCESS_KEY: test
      QUEUE_NAME: tratar-ativos
      LOG_LEVEL: INFO
      RETRY_ATTEMPTS: 3
      RETRY_DELAY: 10

volumes:
  mysql_data:
  localstack_data:


````


Arquitetura e fluxo de dados
---------------------------
1. Provisionamento (opcional) — `terraform` cria recursos (em localstack para dev).
2. Producer/Producer-like (p.ex. outros componentes) enviam mensagens para SQS `tratar-ativos`.
3. `gestor-ativos-brutos` consome/valida mensagens, pode enriquecer dados via BRAPI e publicar eventos.
4. `gerar-insights` (Python worker) consome a fila `tratar-ativos`, realiza análises (mean reversion, momentum, valuation) e persiste resultados em MySQL.
5. Métricas e healthchecks expostos pelo Java via Spring Actuator; logs em volume compartilhado.

Componentes principais (local)
- `localstack` (SQS) — endpoint: 4566
- `mysql` — banco de dados (schema em `mysql-init/`)
- `gestor-ativos-brutos` — porta HTTP exposta: 8091 (container)
- `gerar-insights` — porta HTTP exposta: 8080 (worker/API)

Execução rápida (com Docker Compose)
-----------------------------------
1. Copie/ajuste um `.env` local (exemplo abaixo).
2. Suba os serviços:
```bash
docker compose up --build
## ️ Componentes e Tecnologias

### 1. Gestor Ativos Brutos (Java 21 + Spring Boot 3)
O núcleo do sistema. Responsável por:
- Exposição da API REST para usuários.
- Integração com a API Brapi para cotações.
- Orquestração de mensagens via SQS.
- Consolidação de dados para análise de IA.
- **Tecnologias**: Spring WebFlux, JPA/Hibernate, AWS SDK, Google GenAI SDK.

### 2. Gerar Insights (Python 3.12)
Worker especializado em cálculos matemáticos e fundamentalistas:
- Consome mensagens da fila `tratar-ativos`.
- Calcula Preço Justo de Graham e Margens de Segurança.
- Persiste os resultados brutos no MySQL para posterior análise da IA.
- **Tecnologias**: Boto3, MySQL Connector, Pydantic.

### 3. Infraestrutura & Mensageria
- **LocalStack**: Emula o ambiente AWS (SQS) localmente.
- **Terraform**: Automatiza a criação das filas e permissões.
- **MySQL 8.0**: Base de dados central para histórico e insights calculados.

##  Como Executar

### Pré-requisitos
- Docker & Docker Compose
- Chave de API do Gemini (Google AI Studio)

### Configuração
Crie um arquivo `.env` na raiz ou exporte a variável:
```bash
export GEMINI_API_KEY=sua_chave_aqui
```

### Inicialização
```bash
# Sobe todo o ecossistema
docker-compose up -d --build
```

##  Endpoints Principais

### Monitoramento de Ativos
- `GET /ativos/{simbolo}`: Retorna a cotação atual e dados da empresa.
- `POST /ativos/registrar/{simbolo}`: Adiciona o ativo à fila de monitoramento periódico.

### Inteligência Artificial (Insights)
- `GET /insights/{simbolo}/analise`: Consolida os dados fundamentalistas calculados pelo worker Python e gera uma análise qualitativa via Gemini.
    - **Header Opcional**: `X-Gemini-Key` para usar uma chave dinâmica.

## ⚙️ Configurações Importantes e Variáveis Dinâmicas

Todo o ecossistema é altamente configurável de forma dinâmica por meio de variáveis de ambiente. Ao disponibilizar as imagens no Docker Hub ou ao executá-las localmente, você pode customizar os seguintes parâmetros:

### Variáveis Globais (Infraestrutura)
| Variável | Descrição | Valor Padrão                             |
|----------|-----------|------------------------------------------|
| `SERVER_PORT` | Porta onde o serviço Java escutará | `8091`                                   |
| `AWS_SQS_ENDPOINT_BASE` | Endpoint do LocalStack | `http://localstack:4566`                 |
| `GEMINI_API_KEY` | Chave de acesso ao Google Gemini | `<SUA_CHAVE_AQUI>` (Default de fallback) |

### Variáveis do Banco de Dados (MySQL)
| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `DB_URL` / `DB_HOST` | URL/Host de conexão com o MySQL | `jdbc:mysql://mysql:3306/minha_base` / `mysql` |
| `DB_USERNAME` / `DB_USER` | Usuário de conexão do banco | `spring` |
| `DB_PASSWORD` / `DB_PASS` | Senha de conexão do banco | `spring123` |
| `DB_NAME` | Nome do schema no MySQL | `minha_base` |

> [!TIP]
> Você pode passar essas variáveis diretamente no arquivo `.env` da raiz ou no bloco `environment` do seu `docker-compose.yml` para que as imagens se autoconfigurem dinamicamente com base nas suas credenciais reais de banco ou provedor de nuvem.

##  Arquivos de exemplo de variáveis de ambiente (imagens)

Para facilitar a execução das imagens Docker e a configuração local, o repositório contém arquivos de exemplo com as variáveis necessárias para cada serviço.

- `gerar-insights/.env.example` — variáveis usadas pelo worker Python em execução local
- `gerar-insights/env/.env.docker.example` — variáveis para execução dentro do container (usadas por `ENVIRONMENT=docker`)
- `gestor-ativos-brutos/.env.example` — variáveis para a aplicação Java (Spring Boot)

Copie o arquivo de exemplo adequado e ajuste os valores antes de subir o ambiente. Exemplo:

```bash
cp gerar-insights/.env.example gerar-insights/.env.local
cp gerar-insights/env/.env.docker.example gerar-insights/env/.env.docker
cp gestor-ativos-brutos/.env.example gestor-ativos-brutos/.env
```

Esses arquivos permitem que as imagens sejam executadas sem a necessidade de editar o `docker-compose.yml`.

##  Documentação Técnica
A especificação completa da API pode ser encontrada no arquivo [openapi.yaml](./openapi.yaml).
