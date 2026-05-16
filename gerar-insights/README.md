# Gerar Insights (Motor Financeiro)

Aplicação Python responsável por ser o **Cérebro Analítico** do ecossistema. Operando como um worker assíncrono em loop infinito, ele consome snapshots de ativos brutos de uma fila SQS, aplica matemática financeira e grava o resultado histórico e estratégico no banco relacional.

## Responsabilidades e Valor Gerado
1. **Consumo Robusto (SQS)**: Lê mensagens sem gerar gargalos, processando e apagando de forma rápida.
2. **Histórico Bruto**: Guarda a "foto" de mercado do dia do ativo (`historico_acoes`).
3. **Cálculo Estratégico (Insights)**: Utilizando o `FinancialAnalyzerService`, ele extrai o **Preço Justo (Benjamin Graham)**, a **Margem de Segurança** (%) e aplica uma heurística de recomendação final (COMPRA/VENDA/NEUTRO). Esse insight de alto valor é armazenado na tabela `insight_acao`.

## Libs Principais Utilizadas
- **boto3**: SDK AWS para a escuta e manipulação segura da fila SQS.
- **SQLAlchemy + PyMySQL**: Utilizado para gerenciar conexões ao MySQL, mapeamento objeto-relacional (ORM) e persistência de dados.
- **python-dotenv**: Responsável por injetar variáveis de ambiente locais ao rodar fora do Docker.
- **python-json-logger**: Padronização dos logs no formato estruturado para melhor observabilidade.

## Variáveis de Ambiente e Configuração
A aplicação carrega nativamente variáveis baseadas no `ENVIRONMENT`.

| Variável | Padrão (Local) | Descrição |
| --- | --- | --- |
| `ENVIRONMENT` | `local` | A chave central. Se configurado como `docker`, a aplicação muda os alvos do SQS e DB para `localstack` e `mysql` internos. |
| `DB_HOST` / `DB_PORT` | `localhost:3305` | Endereço do banco. Muda automaticamente para `mysql:3306` se `ENVIRONMENT=docker`. |
| `LOCALSTACK_ENDPOINT` | `http://localhost:4566` | Endereço da fila SQS AWS emulada. |
| `QUEUE_NAME` | `tratar-ativos` | Fila lida em loop pela aplicação. |

## Como Rodar

**1. Ambiente de Desenvolvimento (IDE / Local)**
Para trabalhar isoladamente nesta aplicação sem conflitar com a rede Docker:
Crie um arquivo `.env.local` na raiz e execute o projeto (tendo o banco e localstack rodando).
```bash
pip install -r requirements.txt
python main.py
```

**2. Ambiente Docker**
Sem necessidade de intervenção, ele receberá do `docker-compose.yml` as diretrizes.
```bash
docker-compose up -d --build gerar-insights
```
