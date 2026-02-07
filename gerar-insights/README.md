Projeto: gerar-insights

Visão geral

Este repositório contém o serviço "gerar-insights", responsável por processar dados de mercado e produzir insights que alimentam outras partes do ecossistema. O objetivo principal é ler dados (via filas ou banco), transformar em métricas e sinais, e armazenar/expôr esses resultados para consumo. O texto abaixo explica de forma simples como o sistema funciona, quais componentes se integram e as tecnologias envolvidas.

Arquitetura e integração entre componentes

- Entrada: o serviço recebe mensagens através de SQS (ou outra fila configurada). Essas mensagens trazem snapshots ou eventos de mercado.
- Processamento: o núcleo do serviço aplica regras, indicadores e estratégias para gerar insights. Esse processamento fica no pacote `app.core` e suas subpartes (indicadores, estratégias, trading engine).
- Persistência/Enriquecimento: durante ou após o processamento, dados são lidos/escritos em bancos (MySQL é usado no projeto) e/ou DynamoDB (há código para integração com Dynamo na pasta `app.external`). O resultado também pode ser enviado para outros tópicos/filas ou salvo em tabelas para analise posterior.
- Observabilidade: o projeto inclui configuração de logs estruturados para facilitar debug e auditoria.

Fluxo resumido (simples):
1. Mensagem chega na fila (SQS).
2. `entrypoint_sqs` consome a mensagem e chama os serviços de processamento.
3. O core aplica indicadores e produz resultados (`app.core.insights`, `trading_engine`).
4. Resultados são armazenados no banco e/ou Dynamo e, se necessário, publicados para outros consumidores.

Componentes principais

- `entrypoint/` — pontos de entrada para o serviço (ex.: SQS).
- `core/` — lógica de negócio: indicadores, geração de insights e mecanismo de trading.
- `external/` — adaptadores para serviços externos (DynamoDB, banco, etc.).
- `config/` — configurações, detectores de ambiente e logger.
- `dto/` — objetos de transporte (por exemplo, `market_data.py`).
- `tests/` — testes unitários e de integração já presentes no projeto.

Tecnologias utilizadas

Com base nos arquivos do projeto (especialmente `requirements.txt`) e na estrutura de pastas, as tecnologias principais são:

- Linguagem: Python 3.x (código atual compatível com versões recentes).
- Filas: AWS SQS (integração via `boto3`).
- Banco de dados relacional: MySQL (driver `pymysql`, SQLAlchemy para ORM/engine).
- NoSQL: DynamoDB (há um serviço `dynamo_service.py`).
- Configuração e ambiente: `python-dotenv` para variáveis de ambiente.
- Validação/Modelos: `pydantic` para DTOs e validação de dados.
- Logging: `python-json-logger` para logs estruturados.
- Requisições HTTP: `requests` (para chamadas externas, se necessário).

Como rodar (rápido)

1) Criar um ambiente virtual e instalar dependências:

```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt
```

2) Ajustar variáveis de ambiente (usar `.env` ou variáveis do sistema) com credenciais AWS, string de conexão do MySQL e outras configurações encontradas em `app/config`.

3) Executar o entrypoint localmente (exemplo):

```powershell
python main.py
```

Observação: dependendo da configuração, o serviço pode estar pensado para rodar em container (há `Dockerfile`) e/ou ser orquestrado via `docker-compose` do diretório raiz.

Estrutura de pastas (resumida)

- gerar-insights/
  - app/: código fonte do serviço
  - env/: exemplos de variáveis de ambiente (se houver)
  - output_charts/: gráficos/artefatos gerados
  - tests/: testes automatizados
  - Dockerfile, requirements.txt, main.py

Testes

Existem testes em `tests/` (unitários e de integração). Para rodar os testes localmente, assegure que as dependências estejam instaladas e execute o runner de testes que preferir (pytest é o mais provável; caso não exista `pytest` em `requirements.txt`, adicionar pode ser útil).

Contribuição

Sinta-se livre para abrir issues ou pull requests. Se for submeter mudanças maiores, prefira abrir um issue primeiro descrevendo a intenção, porque algumas partes do domínio (estratégias, indicadores) são sensíveis e podem quebrar o comportamento esperado.

Licença

O repositório não inclui uma licença explícita neste README. Se for publicar no GitHub, pense em adicionar um arquivo `LICENSE` com a licença desejada.

Notas finais (tom coloquial)

Este README tenta explicar de maneira simples o que o projeto faz e como as peças se encaixa, mas pode faltar detalhe fino de configuração (ex.: nomes exatos de filas, tabelas e variáveis de ambiente). Para rodar em produção, cheque os arquivos em `app/config` e as variáveis esperadas. Se algo ficou confuso, me diga que eu ajeito ou complemento com exemplos mais técnicos.

Este README foi movido para o raiz do repositório.
Por favor, consulte `../README.md` para uma visão geral do projeto, instruções de execução e informações sobre a aplicação Java (`gestor-ativos-brutos`) e outros artefatos.
