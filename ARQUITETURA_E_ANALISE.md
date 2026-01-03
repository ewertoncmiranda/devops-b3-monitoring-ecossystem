# 📊 Análise Completa do Projeto DevOps Study

**Data:** 2026-01-03  
**Versão:** 1.0

---

## 📋 Índice

1. [Visão Geral do Projeto](#visão-geral)
2. [Arquitetura e Componentes](#arquitetura)
3. [Fluxo de Dados](#fluxo-de-dados)
4. [Dependências e Recursos](#dependências)
5. [Estrutura de Classes e Componentes](#estrutura-de-classes)
6. [Problemas Identificados](#problemas-identificados)
7. [Plano de Refatoração](#plano-de-refatoração)
8. [Testes Propostos](#testes-propostos)

---

## 🎯 Visão Geral do Projeto {#visão-geral}

### Propósito
Sistema de análise de ativos da B3 (Bolsa de Valores Brasileira) com coleta de dados, persistência em banco de dados e geração de insights com recomendações de trading (compra/venda/manter).

### Componentes Principais
- **Java/Spring Boot**: Serviço `gestor-ativos-brutos` - Busca dados da API Brapi e envia para fila SQS
- **Python**: Serviço `gerar-insights` - Consome mensagens da fila, processa indicadores e gera insights
- **MySQL**: Persistência de histórico de ativos
- **LocalStack**: Emula AWS (SQS, DynamoDB, S3)
- **Docker Compose**: Orquestração de todos os serviços

### Stack Tecnológico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| **Backend (Gestor)** | Java/Spring Boot | 21 / 3.3.0 |
| **Worker (Insights)** | Python | 3.11 |
| **Banco de Dados** | MySQL | 8.0 |
| **Message Queue** | AWS SQS/LocalStack | 3.3 |
| **NoSQL** | DynamoDB (LocalStack) | - |
| **Container Orchestration** | Docker Compose | 3.8 |
| **ORM** | SQLAlchemy (Python) / JPA (Java) | Latest |

---

## 🏗️ Arquitetura e Componentes {#arquitetura}

### Diagrama Arquitetural

```
┌─────────────────────────────────────────────────────────────┐
│                      DevOps Study                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  API Brapi (B3)  │         │  HTTP Clients    │          │
│  └────────┬─────────┘         └────────┬─────────┘          │
│           │                            │                     │
│           └────────────┬───────────────┘                     │
│                        │                                      │
│            ┌───────────▼──────────────┐                      │
│            │ GESTOR-ATIVOS-BRUTOS    │                      │
│            │  (Java/Spring Boot)      │                      │
│            │  Port: 8091              │                      │
│            └────────────┬──────────────┘                     │
│                         │                                     │
│          ┌──────────────┴──────────────┐                     │
│          │                             │                     │
│    ┌─────▼──────┐            ┌────────▼────────┐            │
│    │   MySQL    │            │   SQS Queue     │            │
│    │ Port: 3305 │            │ (tratar-ativos) │            │
│    └────────────┘            └────────┬────────┘            │
│                                       │                      │
│                            ┌──────────▼──────────┐           │
│                            │ GERAR-INSIGHTS      │           │
│                            │  (Python/Worker)    │           │
│                            │  Port: 8080         │           │
│                            └──────────┬──────────┘           │
│                                       │                      │
│                    ┌──────────────────┴──────────────────┐   │
│                    │                                     │   │
│            ┌──────▼──────┐                  ┌─────────▼─┐   │
│            │   DynamoDB  │                  │ Histórico │   │
│            │ (insights)  │                  │  MySQL    │   │
│            └─────────────┘                  └───────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Dados {#fluxo-de-dados}

### Fluxo Completo de um Ativo

```
1. REQUEST ENTRADA
   ├─ Cliente HTTP → POST /ativos → AtivoController

2. BUSCA E SALVAMENTO
   ├─ AtivoController.cadastrarNovoAtivo()
   ├─ AtivoServiceService.salvar(codAtivo)
   ├─ ConsultaBrApiService.executar(symbol)
   ├─ API Brapi → retorna dados do ativo
   ├─ AtivoRepository.save() → MySQL
   ├─ Utils.toJson() → Serializa ativo
   └─ QueueConnectImpl.enviarMensagemParaFila()

3. ENFILEIRAMENTO (SQS)
   ├─ SendMessageRequest → AWS SQS
   ├─ Mensagem JSON armazenada na fila "tratar-ativos"
   └─ ACK recebido (SendMessageResponse)

4. CONSUMO (Python Worker)
   ├─ entrypoint_sqs.consume_messages()
   ├─ sqs.receive_message() → máx 10 msgs a cada 10s
   ├─ Itera sobre cada mensagem
   └─ Para cada mensagem:

5. PROCESSAMENTO DE INSIGHTS
   ├─ processar_info(ativo)
   │  ├─ insight_single(ativo)
   │  ├─ TradingService.processar_ativo(ativo)
   │  │  ├─ calcular_indicadores() → dict de métricas
   │  │  ├─ calcular_decisao() → COMPRAR/VENDER/MANTER
   │  │  └─ gerar_insights() → lista de insights textuais
   │  └─ Log dos resultados

6. PERSISTÊNCIA (Histórico)
   ├─ processar_persistencia(ativo)
   ├─ SnapshotAcao(ativo) → Mapper DTO→Entidade
   ├─ PersistenciaHistoricoService.registrar_snapshot()
   ├─ HistoricoAcaoEntity criada
   └─ HistoricoRepository.salvar() → MySQL

7. ORQUESTRAÇÃO DE MÉTRICAS (A cada 2 min)
   ├─ ProcessamentoMetricasOrchestrator.run()
   ├─ DatabaseService.get_all_symbols()
   ├─ Para cada símbolo:
   │  ├─ get_latest_snapshot()
   │  ├─ get_last_n_registros_ativos() → últimos 30 registros
   │  ├─ AggregatorService.aggregate() → contexto enriquecido
   │  ├─ TradingService.processar_ativo() → análise completa
   │  └─ resultado_final.append()
   ├─ JSON.dumps() com EnhancedJSONEncoder
   ├─ Log de saída rica
   └─ Sleep 120 segundos

8. ARMAZENAMENTO FINAL
   ├─ DynamoDB (insights refinados) → dynamo_service.salvar_insights_em_dynamodb()
   └─ MySQL (histórico) → histórico_entity
```

---

## 📦 Dependências e Recursos {#dependências}

### Java/Spring Boot (gestor-ativos-brutos)

```
Dependências Principais:
├─ org.springframework.boot:spring-boot-starter-webflux     [REST Assíncrono]
├─ org.springframework.boot:spring-boot-starter-web         [REST/Controllers]
├─ org.springframework.boot:spring-boot-starter-data-jpa    [ORM]
├─ mysql:mysql-connector-java:8.0.33                       [BD]
├─ software.amazon.awssdk:sqs:2.31.68                      [SQS]
├─ org.springframework.cloud:spring-cloud-starter-openfeign [HTTP Client]
├─ org.projectlombok:lombok:1.18.38                        [Boilerplate]
└─ org.modelmapper:modelmapper:3.1.1                       [DTO→Entity]

Recursos:
├─ HTTP: WebClient + RestTemplate
├─ Database: JPA Repository
├─ Queue: AWS SDK SQS Client
├─ Logging: Spring Logger
└─ Configuration: application.properties
```

### Python (gerar-insights)

```
Dependências (requirements.txt):
├─ pymysql                    [MySQL Driver]
├─ boto3==1.26.149           [AWS SDK]
├─ botocore==1.29.149        [AWS Core]
├─ requests>=2.28.0          [HTTP Client]
├─ numpy                      [Cálculos Numéricos]
├─ sqlalchemy                 [ORM]
└─ matplotlib                 [Gráficos]

Recursos:
├─ SQS Client (boto3)
├─ DynamoDB Client (boto3)
├─ SQLAlchemy ORM + SessionLocal
├─ Logging setup
└─ MySQL Connection
```

### Infraestrutura (Docker Compose)

```
Serviços:
├─ localstack:3.3             [SQS, DynamoDB, S3, SecretsManager]
├─ mysql:8.0                  [Banco de Dados]
├─ gestor-ativos-brutos       [Java Service]
└─ gerar-insights             [Python Service]

Volumes:
├─ mysql_data:/var/lib/mysql                 [Persistência MySQL]
├─ localstack_data:/var/lib/localstack       [Persistência LocalStack]
├─ ./logs/java:/var/log/myapp               [Logs Java]
├─ ./logs/python:/var/log/pyapp             [Logs Python]
└─ ./gerar-insights/output_charts:/app/output_charts [Gráficos]

Redes:
└─ default (docker network)
```

---

## 🏛️ Estrutura de Classes e Componentes {#estrutura-de-classes}

### Java - gestor-ativos-brutos

```
br.com.miranda.gestor.ativos.brutos/
│
├── TheMachineApplication (Main)
│   └─ @SpringBootApplication
│
├── config/
│   └── ConfigSqs
│       └─ @Bean SqsClient: Configura cliente SQS com LocalStack
│
├── service/
│   ├── ConsultaBrApiService
│   │   └─ executar(symbol): BrapiResponseDTO
│   │      └─ Requisição HTTP para Brapi com Headers
│   │
│   └── AtivoServiceService implements AtivoServicePort
│       ├─ salvar(codAtivo): Ativo
│       │  ├─ buscarPorSymbol()
│       │  ├─ Map BrapiAtivoDTO → Ativo (ModelMapper)
│       │  ├─ ativoRepository.save()
│       │  ├─ Utils.toJson()
│       │  └─ queueConnectPort.enviarMensagemParaFila()
│       │
│       └─ buscarPorSymbol(symbol): BrapiResponseDTO
│
├── entrypoint/
│   └── controller/
│       ├── AtivoController
│       │   ├─ GET /ativos/{ativo}: BrapiResponseDTO
│       │   └─ POST /ativos: Ativo
│       │
│       └── QueueController
│           └─ GET /fila: ResponseEntity<String>
│              └─ Teste da fila SQS
│
├── external/
│   ├── queue/
│   │   └── QueueConnectImpl implements QueueConnectPort
│   │       └─ enviarMensagemParaFila(mensagem): String
│   │          ├─ SendMessageRequest.builder()
│   │          └─ sqsClient.sendMessage()
│   │
│   ├── database/
│   │   ├── entidade/
│   │   │   └── Ativo
│   │   │       └─ @Entity @Table("ativos")
│   │   │          ├─ symbol, currency, shortName, longName
│   │   │          ├─ marketCap, regularMarketPrice
│   │   │          ├─ regularMarketChange, regularMarketChangePercent
│   │   │          ├─ regularMarketOpen, regularMarketDayHigh, regularMarketDayLow
│   │   │          ├─ regularMarketVolume, regularMarketPreviousClose
│   │   │          ├─ fiftyTwoWeekLow, fiftyTwoWeekHigh
│   │   │          ├─ priceEarnings, earningsPerShare
│   │   │          ├─ logoUrl, regularMarketTime
│   │   │          └─ regularMarketDayRange, fiftyTwoWeekRange
│   │   │
│   │   └── repository/
│   │       └── AtivoRepository extends JpaRepository<Ativo, Long>
│   │
│   └── dto/
│       ├── BrapiResponseDTO
│       │   └─ results: List<BrapiAtivoDTO>
│       │
│       └── BrapiAtivoDTO (alinha com Ativo)
│
├── port/
│   ├── AtivoServicePort (Interface)
│   │   ├─ salvar(ativo): Ativo
│   │   └─ buscarPorSymbol(symbol): BrapiResponseDTO
│   │
│   └── QueueConnectPort (Interface)
│       └─ enviarMensagemParaFila(mensagem): String
│
└── tools/
    └── Utils
        └─ toJson(object): String
```

### Python - gerar-insights

```
gerar-insights/
│
├── main.py (Entrypoint)
│   ├─ wait_for_mysql(engine)
│   ├─ criar_tabelas()
│   ├─ ensure_queue(QUEUE_NAME)
│   └─ consume_messages(queue_url)
│
├── app/
│   │
│   ├── config/
│   │   ├── aws_config.py
│   │   │   ├─ boto3 SQS Client
│   │   │   ├─ boto3 DynamoDB Resource
│   │   │   └─ Configuração LocalStack (endpoint, región, credenciais)
│   │   │
│   │   ├── database_config.py
│   │   │   ├─ SQLAlchemy engine
│   │   │   └─ SessionLocal = sessionmaker
│   │   │
│   │   ├── config_logger.py
│   │   │   └─ setup_logger(): Configuração de logging
│   │   │
│   │   ├── timeout_db_engine.py
│   │   │   └─ wait_for_mysql(engine, retries, delay)
│   │   │      └─ Retry de conexão com timeout
│   │   │
│   │   └── enhanced_json.py
│   │       └─ EnhancedJSONEncoder(json.JSONEncoder)
│   │          └─ default(): Serializa Decimal, numpy types
│   │
│   ├── core/
│   │   ├── mapper/
│   │   │   └── equity_snapshot.py
│   │   │       └─ SnapshotAcao(payload: dict)
│   │   │          ├─ simbolo, preco_abertura, preco_fechamento
│   │   │          ├─ preco_maximo, preco_minimo, volume
│   │   │          ├─ minima_52_semanas, maxima_52_semanas
│   │   │          ├─ valor_mercado, preco_lucro, lucro_por_acao
│   │   │          └─ __repr__()
│   │   │
│   │   ├── service/
│   │   │   ├── trading_service.py
│   │   │   │   └─ TradingService
│   │   │   │      ├─ processar_ativo(ativo): (decisao, indicadores, insights)
│   │   │   │      ├─ calcular_indicadores(ativo): dict
│   │   │   │      │  ├─ oscilacao_dia_percentual
│   │   │   │      │  ├─ variacao_abertura
│   │   │   │      │  ├─ pl, lpa, earnings_yield
│   │   │   │      │  ├─ valor_mercado
│   │   │   │      │  ├─ range_52_semanas
│   │   │   │      │  ├─ posicao_no_range_52w_percent
│   │   │   │      │  └─ volume_hoje
│   │   │   │      ├─ calcular_decisao(indicadores): str
│   │   │   │      │  └─ Regras:
│   │   │   │      │     ├─ earnings_yield > 12% → COMPRAR
│   │   │   │      │     ├─ variacao_abertura < -3% → VENDER
│   │   │   │      │     └─ else → MANTER
│   │   │   │      │
│   │   │   │      └─ gerar_insights(indicadores): list[str]
│   │   │   │         └─ Análise de:
│   │   │   │            ├─ Lucro relativo
│   │   │   │            ├─ Proximidade de máximas/mínimas de 52w
│   │   │   │            ├─ Volatilidade do dia
│   │   │   │            └─ Sinais de tendência
│   │   │   │
│   │   │   ├── persistencia_service.py
│   │   │   │   └─ PersistenciaHistoricoService
│   │   │   │      ├─ __init__: HistoricoRepository
│   │   │   │      └─ registrar_snapshot(db, snapshot)
│   │   │   │         ├─ SnapshotAcao → HistoricoAcaoEntity
│   │   │   │         └─ repository.salvar()
│   │   │   │
│   │   │   ├── aggregator_service.py
│   │   │   │   └─ AggregatorService
│   │   │   │      └─ @staticmethod aggregate(symbol, snapshot, historico)
│   │   │   │         └─ Retorna contexto enriquecido:
│   │   │   │            ├─ snapshot (preço, volume, índices)
│   │   │   │            └─ historico (média, máx, mín, vol médio)
│   │   │   │
│   │   │   ├── indicator_service.py (Vazio)
│   │   │   │
│   │   │   └── insight_service.py (Vazio)
│   │   │
│   │   └── strategies/
│   │       └─ (Pasta com estratégias - não explorada)
│   │
│   ├── dto/
│   │   └── market_data.py (Explorar se necessário)
│   │
│   ├── entrypoint/
│   │   ├── entrypoint_sqs.py
│   │   │   ├─ ensure_queue(name): str
│   │   │   │  └─ Valida e retorna URL da fila
│   │   │   │
│   │   │   ├─ consume_messages(queue_url)
│   │   │   │  └─ Loop infinito:
│   │   │   │     ├─ sqs.receive_message(MaxMessages=10, WaitTime=10s)
│   │   │   │     ├─ Para cada mensagem:
│   │   │   │     │  ├─ json.loads(Body)
│   │   │   │     │  ├─ processar_info(ativo)
│   │   │   │     │  ├─ processar_persistencia(ativo)
│   │   │   │     │  ├─ processar_metricas.run()
│   │   │   │     │  └─ sqs.delete_message() ✓
│   │   │   │     └─ sleep(30s)
│   │   │   │
│   │   │   ├─ processar_persistencia(ativo)
│   │   │   │  └─ Cria snapshot e persiste no histórico
│   │   │   │
│   │   │   └─ insight_single(ativo)
│   │   │      └─ TradingService().processar_ativo()
│   │   │
│   │   └── processamento_metricas.py
│   │       └─ ProcessamentoMetricasOrchestrator
│   │          ├─ __init__:
│   │          │  ├─ DatabaseService
│   │          │  ├─ AggregatorService
│   │          │  └─ TradingService
│   │          │
│   │          └─ run()
│   │             ├─ get_all_symbols()
│   │             ├─ Para cada símbolo:
│   │             │  ├─ get_latest_snapshot()
│   │             │  ├─ get_last_n_registros_ativos(symbol, 30)
│   │             │  ├─ aggregate(symbol, snapshot, historico)
│   │             │  ├─ processar_ativo(snapshot)
│   │             │  └─ resultado_final.append()
│   │             ├─ json.dumps(resultado_final, ...)
│   │             └─ sleep(120s)
│   │
│   └── external/
│       ├── dynamo_service.py
│       │   ├─ to_dynamo_safe(value): Converte tipos para DynamoDB
│       │   └─ salvar_insights_em_dynamodb(ativo, insights)
│       │      └─ dynamodb.put_item()
│       │
│       └── database/
│           ├── config/
│           │   └── create_tables.py
│           │       └─ criar_tabelas()
│           │          ├─ historico.metadata.create_all()
│           │          └─ ativos.metadata.create_all()
│           │
│           ├── entity/
│           │   ├── ativos_entity.py
│           │   │   └─ AtivoEntity @declarative
│           │   │      └─ Table: ativos
│           │   │         ├─ Mesmas colunas da entidade Java
│           │   │         └─ __repr__()
│           │   │
│           │   └── historico_entity.py
│           │       └─ HistoricoAcaoEntity @declarative
│           │          └─ Table: historico_acoes
│           │             ├─ simbolo, timestamp
│           │             ├─ preco_abertura, preco_fechamento
│           │             ├─ preco_maximo, preco_minimo, volume
│           │             ├─ minima_52_semanas, maxima_52_semanas
│           │             ├─ valor_mercado, preco_lucro, lucro_por_acao
│           │             └─ criado_em
│           │
│           ├── repository_history.py
│           │   └─ HistoricoRepository
│           │      └─ salvar(db, entidade): HistoricoAcaoEntity
│           │
│           └── insights_repository.py
│               └─ DatabaseService
│                  ├─ get_all_symbols(): list[str]
│                  ├─ get_last_n_registros_ativos(symbol, n=30): list
│                  └─ get_latest_snapshot(symbol): AtivoEntity
│
└── output_charts/ (Pasta para gráficos matplotlib)
```

---

## ⚠️ Problemas Identificados {#problemas-identificados}

### 1. **Inconsistência de Mapeamento (Python)**
- **Problema**: Em `aggregator_service.py`, usa-se snake_case (`regular_market_price`)
- **Local**: `aggregator_service.py` linha ~20
- **Impacto**: AttributeError ao tentar acessar atributos inexistentes
- **Solução**: Padronizar nomenclatura com a entidade

### 2. **Falta de Tratamento de Exceções**
- **Problema**: Muitos `except` genéricos sem logging específico
- **Local**: `entrypoint_sqs.py` linha ~40 (catch Exception em loop)
- **Impacto**: Erros silenciosos, difícil debug
- **Solução**: Criar exceções customizadas

### 3. **DynamoDB não é usado**
- **Problema**: `dynamo_service.py` existe mas nunca é chamado
- **Local**: Órfão no código
- **Impacto**: Overhead desnecessário
- **Solução**: Integrar ou remover

### 4. **SQLAlchemy: Dois Bases declarativos**
- **Problema**: `ativos_entity` e `historico_entity` têm `Base` separados
- **Local**: `entity/ativos_entity.py` e `entity/historico_entity.py`
- **Impacto**: Pode causar conflitos em migrações futuras
- **Solução**: Usar um único Base centralizado

### 5. **Falta de Validação de Entrada**
- **Problema**: Sem validação de campos obrigatórios
- **Local**: `SnapshotAcao.__init__()` aceita qualquer dict
- **Impacto**: Dados incompletos podem ser persistidos
- **Solução**: Adicionar Pydantic ou validação manual

### 6. **Timeout na Fila (Loop Infinito)**
- **Problema**: `consume_messages()` tem timeout 10s mas sleep 30s
- **Local**: `entrypoint_sqs.py` linha ~25
- **Impacto**: Consumo desnecessário de recursos
- **Solução**: Ajustar estratégia de polling

### 7. **Hardcoded API Key**
- **Problema**: Chave da API Brapi em texto plano no código Java
- **Local**: `ConsultaBrApiService.java` linha ~17
- **Impacto**: Segurança comprometida
- **Solução**: Usar variáveis de ambiente ou AWS Secrets Manager

### 8. **Falta de Testes Unitários**
- **Problema**: Nenhum teste unitário presente
- **Local**: Não existe `/test`
- **Impacto**: Confiabilidade questionável
- **Solução**: Implementar testes com pytest (Python) e JUnit (Java)

### 9. **Indicadores de Trading Muito Simplificados**
- **Problema**: Apenas 2 regras básicas de decisão
- **Local**: `trading_service.py` linha ~50
- **Impacto**: Análise superficial
- **Solução**: Adicionar indicadores técnicos (RSI, MACD, SMA)

### 10. **Falta de Índices no Banco de Dados**
- **Problema**: Schema SQL sem índices
- **Local**: `mysql-init/1 - schema.sql`
- **Impacto**: Queries lentas conforme cresce o volume
- **Solução**: Adicionar índices em `symbol`, `timestamp`

---

## 🔧 Plano de Refatoração {#plano-de-refatoração}

### Fase 1: Correções Críticas
1. Unificar Bases SQLAlchemy
2. Fixar AttributeError em AggregatorService
3. Migrar Chave API para variáveis de ambiente
4. Melhorar tratamento de exceções

### Fase 2: Melhorias de Qualidade
5. Adicionar validações com Pydantic
6. Implementar testes unitários (pytest + JUnit)
7. Adicionar índices ao banco de dados
8. Integrar DynamoDB ou remover

### Fase 3: Otimizações
9. Implementar indicadores técnicos avançados
10. Adicionar logging estruturado
11. Health checks e métricas
12. Documentação automática (OpenAPI)

---

## 🧪 Testes Propostos {#testes-propostos}

### Python Tests (pytest)
- `test_trading_service.py`: Testa calcular_indicadores, calcular_decisao, gerar_insights
- `test_snapshot_mapper.py`: Testa SnapshotAcao com payloads variados
- `test_aggregator_service.py`: Testa aggregação de dados
- `test_persistence_service.py`: Testa persistência com mock SQLAlchemy
- `test_sqs_consumer.py`: Testa consumo de mensagens (mock SQS)

### Java Tests (JUnit)
- `AtivoServiceServiceTest`: Testa busca e salvamento
- `AtivoControllerTest`: Testa endpoints REST
- `ConsultaBrApiServiceTest`: Testa integração Brapi (mock HTTP)
- `QueueConnectImplTest`: Testa envio para fila (mock SQS)

### Integração (Docker Compose)
- Script de teste E2E: POST /ativos → fila → consumer → MySQL

---

## 📊 Resumo Executivo

| Aspecto | Status | Prioridade |
|--------|--------|-----------|
| Documentação Código | ❌ Mínima | 🔴 Alta |
| Testes Unitários | ❌ Nenhum | 🔴 Crítica |
| Tratamento Exceções | ⚠️ Genérico | 🔴 Alta |
| Validação Entrada | ❌ Nenhuma | 🟡 Média |
| Segurança | ⚠️ Keys Hardcoded | 🔴 Crítica |
| Performance | ⚠️ Sem Índices | 🟡 Média |
| Indicadores Trading | ⚠️ Básico | 🟡 Média |
| Arquitetura | ✅ Sólida | 🟢 OK |

---

**Próximos Passos**: Implementar refatorações e testes conforme descrito nos planos de fase 1 e 2.

