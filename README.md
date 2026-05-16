# DevOps B3 Monitoring Ecosystem

Bem-vindo ao ecossistema de monitoramento de ativos da B3. Este projeto é composto por múltiplos microserviços e componentes de infraestrutura focados na captura, mensageria e extração de valor de indicadores financeiros.

## Componentes do Sistema

1. **gerenciador-filas (Python)**: Um worker utilitário responsável por interagir com o LocalStack para provisionar dinamicamente a infraestrutura de mensageria (filas SQS) do ecossistema.
2. **gerar-insights (Python)**: O coração analítico do sistema. Este worker assíncrono consome as filas SQS e aplica modelos matemáticos fundamentalistas (Fórmula de Graham, Margem de Segurança) sobre ativos brutos para extrair indicações táticas (Compra, Venda, Neutro).
3. **gestor-ativos-brutos (Java/Spring)**: A aplicação principal gerenciadora de domínio.
4. **LocalStack & MySQL**: Infraestrutura local emulada via Docker para hospedar a fila SQS (`tratar-ativos`) e o banco de dados relacional.

## Geração de Valor Financeiro

O serviço `gerar-insights` não apenas armazena dados, mas extrai inteligência real e acionável. Para cada snapshot financeiro lido:
- **Preço Justo (Benjamin Graham)**: Calculado com base no Lucro por Ação (LPA).
- **Margem de Segurança**: Comparação tática entre o preço listado atual do ativo e seu preço justo projetado.
- **Persistência Centralizada**: Toda essa inteligência é armazenada nativamente no schema do MySQL na tabela dedicada `insight_acao`.

## Como Executar

### 1. Tudo pelo Docker (Maneira Mais Fácil)
Isso criará a rede, inicializará os bancos, criará as filas e subirá todos os workers automaticamente.
```bash
docker-compose up -d --build
```
*(Nota: Se houver problemas com as tabelas do MySQL, execute `docker-compose down -v` para apagar os volumes e forçar o script `mysql-init/1 - schema.sql` a rodar).*

### 2. Rodando Serviços Python Localmente (Para Debug/IDE)
Os serviços em Python foram projetados para serem inteligentes. Se executados fora do Docker, eles mudarão a mira automaticamente para apontar para seu `localhost` (consumindo as portas mapeadas pelo Docker).
1. Inicie a infraestrutura: `docker-compose up -d mysql localstack`
2. Configure seus `.env` (veja a seção TODO abaixo).
3. Execute o código: `python main.py`

## TODO: Configuração de Arquivos `.env`

Para garantir um fluxo de desenvolvimento perfeito entre o ambiente dockerizado e a sua IDE local, adote a seguinte configuração:

- [ ] **Configuração Local (`gerar-insights` e `gerenciador-filas`)**:
  Crie arquivos `.env` na raiz dos respectivos projetos contendo credenciais apontadas para o *host local*:
  ```env
  ENVIRONMENT=local
  # Portas mapeadas pelo Docker Compose para a máquina local
  LOCALSTACK_ENDPOINT=http://localhost:4566
  DB_HOST=localhost
  DB_PORT=3305
  DB_USER=spring
  DB_PASS=spring123
  DB_NAME=minha_base
  ```
- [ ] **Configuração Docker**:
  Nenhum `.env` manual é necessário. O `docker-compose.yml` sobrescreve a configuração injetando `ENVIRONMENT: docker`. As aplicações irão automaticamente chavear suas buscas para os serviços internos (`mysql:3306`, `http://localstack:4566`).
