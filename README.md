devops-b3-monitoring-ecossystem

Visão geral

Este repositório agrupa dois serviços principais que compõem um ecossistema de monitoramento e processamento de dados financeiros:

- gerar-insights (Python): serviço responsável por consumir dados de mercado, calcular indicadores e gerar insights. Implementado em Python, consome mensagens (ex.: SQS), processa e persiste resultados.
- gestor-ativos-brutos (Java): aplicação Java/Maven que atua como outro componente do sistema (serviço de domínio, processamento ou API) e que também pode interagir com o mesmo banco ou outros artefatos gerados.

O repositório também inclui infra auxiliar: `docker-compose.yml` para orquestração local, inicializações de banco em `mysql-init/` e scripts em `scripts-aws/` para criar recursos AWS (ex.: SQS).

Arquitetura e integração entre componentes

- Mensageria: AWS SQS é usada para integrar produtores e consumidores (o `gerar-insights` possui um `entrypoint_sqs` para consumir mensagens). Há scripts em `scripts-aws/` que ajudam a criar filas.
- Banco de dados: MySQL é usado como fonte/persistência compartilhada (existem scripts de inicialização em `mysql-init/`). Além disso, há integração com DynamoDB para casos de armazenamento NoSQL (`app/external/dynamo_service.py`).
- Processamento: o serviço Python processa snapshots/eventos e gera sinais/insights; a aplicação Java provê outra peça do domínio que pode consumir os mesmos dados ou servir outra visão do sistema.
- Observabilidade: logs estruturados (JSON) e configuradores estão presentes no código Python; a aplicação Java pode ter sua própria estratégia de logs (ver `gestor-ativos-brutos/src/main/resources`).

Fluxo típico (exemplo simplificado)

1. Produtores publicam eventos/snapshots na fila SQS.
2. `gerar-insights` consome mensagens, calcula indicadores e gera insights.
3. Insights são armazenados em MySQL e, quando aplicável, em DynamoDB.
4. `gestor-ativos-brutos` (ou outro consumidor) pode ler os dados persistidos para relatórios, APIs ou ações de negócio.

Componentes e onde olhar

- ./gerar-insights/: serviço Python (código em `app/`, `main.py`, `Dockerfile`, `requirements.txt`).
- ./gestor-ativos-brutos/: aplicação Java gerenciada por Maven (pom.xml, src/ e target/).
- ./docker-compose.yml: composição local para levantar serviços dependentes.
- ./mysql-init/: scripts SQL para inicializar o schema do banco.
- ./scripts-aws/: exemplos de scripts para criar recursos AWS (SQS, etc.).

Tecnologias utilizadas

- Python 3.x: `boto3`, `sqlalchemy`, `pymysql`, `python-dotenv`, `pydantic`, `python-json-logger`, `requests`.
- Java 17+ (provável): projeto Maven em `gestor-ativos-brutos` (compilar com Maven, empacotar jar).
- Banco de dados: MySQL.
- NoSQL: DynamoDB (quando aplicável).
- Mensageria: AWS SQS.
- Containerização: Docker / Docker Compose.

Como rodar localmente (rápido)

A seguir há passos mínimos para experimentar o projeto em ambiente de desenvolvimento Windows (PowerShell). Ajuste variáveis e caminhos conforme seu ambiente.

1) Usando Docker Compose (recomendado para levantar infra  rapidamente):

```powershell
# Na raiz do repositório
docker-compose up --build
```

Esse comando tenta levantar os serviços descritos em `docker-compose.yml`. Verifique `docker-compose.yml` para ver quais serviços são levantados (banco, filas simuladas, etc.).

2) Rodando apenas o serviço Python (`gerar-insights`) localmente:

```powershell
# entre na pasta do serviço
Set-Location .\gerar-insights
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
# configurar variáveis de ambiente (.env ou variáveis do sistema)
python main.py
```

3) Rodando a aplicação Java (`gestor-ativos-brutos`):

```powershell
# na raiz do repo
Set-Location .\gestor-ativos-brutos
# construir o artefato
mvnw.cmd clean package
# rodar o jar gerado em target/
java -jar .\target\gestor-ativos-brutos-0.0.1-SNAPSHOT.jar
```

Testes

- Python: existem testes em `gerar-insights/tests/`. Recomenda-se usar `pytest` (instale com pip se necessário) e executar `pytest` a partir do diretório `gerar-insights`.
- Java: execute `mvnw.cmd test` dentro de `gestor-ativos-brutos`.

Observações de configuração

- Verifique `gerar-insights/app/config/` para detalhes de variáveis de ambiente esperadas (AWS credentials, DB connection string, nomes de filas, timeouts, etc.).
- Os scripts em `scripts-aws/` são exemplos e podem requerer permissões e contexto AWS corretos.
- Para inicializar o banco localmente, use os scripts em `mysql-init/` ou o `docker-compose` que já referencia esses scripts.

Contribuição

Abra issues para discutir mudanças antes de PRs maiores. Mantenha compatibilidade quando mexer em estratégias/indicadores, pois mudanças podem afetar consumidores.

Licença

Adicione um `LICENSE` se for publicar o projeto em GitHub com uma licença explícita.

Notas finais (tom natural)

Este README foi escrito para fornecer um panorama do repositório como um todo — tanto o serviço Python quanto a aplicação Java — com instruções rápidas para começar. Pode ter falta de detalhes finos de configuração; cheque os arquivos de configuração e os scripts citados para detalhes. Se quiser, eu ajusto o README com exemplos de `.env`, configuração do Docker Compose ou templates de deploy.

