# Gestor de Ativos Brutos (Java Spring Boot)

Aplicação backend robusta desenhada em **Java com Spring Boot**. Seu propósito é atuar como API, ponto de integração ou serviço de domínio dentro do ecossistema de monitoramento financeiro da B3, fazendo a ponte entre sistemas externos, mensageria SQS e a camada de persistência.

## Responsabilidades
1. **Integração de Domínio**: Centralizar endpoints REST e fluxos de injeção ou consulta dos dados financeiros em tempo real.
2. **Mensageria (AWS SQS)**: Capaz de gerar/produzir payloads ou escutar eventos do barramento via abstrações de SQS do ecossistema Spring Cloud AWS.
3. **Persistência Centralizada (MySQL)**: Conecta-se à mesma fonte de dados relacional populada pelo worker (que gerou o schema via `mysql-init`), permitindo abstrair operações CRUD de negócio.

## Libs Principais Utilizadas
- **Spring Boot Core / Spring Web**: Facilitador para levantamento rápido do servidor HTTP e injeção de dependências.
- **Spring Data JPA / Hibernate**: Ferramenta de mapeamento ORM (Object-Relational Mapping) para interagir de forma performática com o MySQL.
- **MySQL Connector / JDBC Driver**: Responsável pela conexão com banco relacional nativa da JVM.
- **Spring Cloud AWS / AWS Java SDK**: Abstração limpa para publicação e leitura segura em filas AWS (SQS) e outros serviços via clients autoconfigurados.
- **Lombok**: Lib que reduz drasticamente código de *boilerplate* em classes de domínio (getters, setters, builders, logs).

## Variáveis de Ambiente e Configuração
O comportamento do framework é altamente dirigido pelos perfis (`application.properties` ou `.env`). 

| Variável / Propriedade | Padrão | Descrição |
| --- | --- | --- |
| `SPRING_PROFILES_ACTIVE` | `dev` | Define qual profile (local/dev/prod) será habilitado. |
| `AWS_SQS_ENDPOINT_BASE` | `http://localhost:4566` | Endpoint local do LocalStack para integração de fila AWS. |
| `AWS_REGION` | `sa-east-1` | Região emulada da infra AWS. |
| Banco de Dados Properties | Porta `3306` (Docker) ou `3305` (Local) | Definido no respectivo `application-{profile}.properties`. |

## Como Executar

**1. Ambiente de Desenvolvimento Local (IDE / Maven)**
Para inicializar o Spring Boot apontando para a infraestrutura do seu docker (MySQL em 3305 e LocalStack em 4566):
```bash
# Baixa as dependências e empacota
./mvnw clean package

# Inicia o projeto com perfil de desenvolvimento
java -jar target/gestor-ativos-brutos-0.0.1-SNAPSHOT.jar
```

**2. Ambiente Docker**
Incluso no `docker-compose.yml`, o container subirá de maneira integrada usando o Dockerfile nativo do projeto, vinculando o banco MySQL e o SQS automaticamente sem conflitos de rede.
