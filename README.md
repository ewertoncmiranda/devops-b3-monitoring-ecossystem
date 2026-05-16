# B3 Monitoring & AI Insights Ecosystem 🚀

Este ecossistema foi projetado para monitorar ativos da bolsa brasileira (B3) em tempo real, processar dados fundamentalistas de forma distribuída e gerar análises preditivas/quantitativas utilizando Inteligência Artificial (Google Gemini).

## 🏗️ Arquitetura do Sistema

O sistema utiliza uma arquitetura baseada em eventos e microserviços, garantindo escalabilidade e resiliência.

```mermaid
graph TD
    User([Usuário]) --> |REST| JavaApp[Gestor Ativos Brutos - Java]
    JavaApp --> |SQL| MySQL[(MySQL 8.0)]
    JavaApp --> |Pub| SQS[[AWS SQS - LocalStack]]
    JavaApp --> |API| Brapi{Brapi API}
    
    SQS --> |Sub| PythonWorker[Gerar Insights - Python]
    PythonWorker --> |Process| Graham[Análise de Graham/Valuation]
    PythonWorker --> |SQL| MySQL
    
    JavaApp --> |Prompt| Gemini[Google Gemini AI]
    Gemini --> |JSON| JavaApp
    
    Infrastructure[Terraform] --> |Provision| SQS
```

## 🛠️ Componentes e Tecnologias

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

## 🚀 Como Executar

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

## 🔌 Endpoints Principais

### Monitoramento de Ativos
- `GET /ativos/{simbolo}`: Retorna a cotação atual e dados da empresa.
- `POST /ativos/registrar/{simbolo}`: Adiciona o ativo à fila de monitoramento periódico.

### Inteligência Artificial (Insights)
- `GET /insights/{simbolo}/analise`: Consolida os dados fundamentalistas calculados pelo worker Python e gera uma análise qualitativa via Gemini.
    - **Header Opcional**: `X-Gemini-Key` para usar uma chave dinâmica.

## ⚙️ Configurações Importantes

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `SERVER_PORT` | Porta do serviço Java | `8091` |
| `AWS_SQS_ENDPOINT_BASE` | Endpoint do LocalStack | `http://localstack:4566` |
| `MYSQL_DATABASE` | Nome da base de dados | `minha_base` |
| `GEMINI_API_KEY` | Chave de acesso ao Google Gemini | - |

## 📄 Documentação Técnica
A especificação completa da API pode ser encontrada no arquivo [openapi.yaml](./openapi.yaml).
