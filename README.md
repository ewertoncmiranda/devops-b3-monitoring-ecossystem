# All Machine DEVOPS Study

- Aplicação centralizada em um docker-compose [ docker-compose up -d]


#### Gestor-ativos-brutos - Java 
 Serviço responsável por buscar ativos na API da B3 , salva na base Mysql e em seguida envia para fila.
 Permite fazer a busca dos detalhes do ativo salvo na base.
        
    Utilizando Serviço :
    GET     http://localhost:8089/ativos/{ativo}
    POST    http://localhost:8089/ativos/ body- código do ativo
   
    POST http://localhost:8089/fila - body
    
    entrypoint estimula fila -> QueueController - endpoint responsável por chamar a fila SQS
    aws.sqs.queue.url=${AWS_SQS_QUEUE_URL:http://localhost:4566/000000000000/tratar-ativos}
    

#### Consulta-bolsa-valores - Python
serviço python baseado em Flask ,responsável por fazer a busca de ativos na B3 
Serviço bate direto na api da B3, chave Hardcode //TODO MUDAR PARA .env  
    
    Usando Serviço:
    GET http://localhost:5000/ativos/MGLU3

    entrypoint -> app/controller.py 
    serviço    -> consulta.py
    dependencia-> requirements.txt


#### gerar-insights - Python
script python ,responsável por escutar a fila SQS tratar-ativos .

    Executar serviço :
    iniciar o arquivo principal -> main.py


````json
version: "3.8"

services:

  localstack:
    image: localstack/localstack:3.3
    container_name: localstack
    environment:
      - SERVICES=sqs,dynamodb,s3,secretsmanager
      - EDGE_PORT=4566
      - AWS_DEFAULT_REGION=sa-east-1
      - DEBUG=1
      - DOCKER_HOST=unix:///var/run/docker.sock
    ports:
      - "4566:4566"
    volumes:
      - localstack_data:/var/lib/localstack
      - ./init-aws:/etc/localstack/init/ready.d
      - /var/run/docker.sock:/var/run/docker.sock
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
    volumes:
      - mysql_data:/var/lib/mysql

  worker-python-infra:
    build:
      context: ./worker-python-infra
    container_name: worker-python-infra
    restart: always
    depends_on:
      - localstack
      - mysql
    environment:
      QUEUE_NAME: tratar-ativos
      QUEUE_NAME_INSIGHTS: tratar-insights
      DYNAMODB_NAME: insights-refinados
      SECRET_NAME: minha-secret
      SECRET_VALUE: kJfyqy8yUVj94SivLsKq4Q
      LOCALSTACK_ENDPOINT: http://localstack:4566
      REGION: sa-east-1
    volumes:
      - ./logs/python:/var/log/pyapp



  gestor-ativos-brutos:
    build:
      context: ./gestor-ativos-brutos
    container_name: gestor-ativos-brutos
    restart: always
    depends_on:
      - mysql
      - worker-python-infra
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/minha_base
      SPRING_DATASOURCE_USERNAME: spring
      SPRING_DATASOURCE_PASSWORD: spring123
      SPRING_SQL_INIT_MODE: never
      AWS_REGION: sa-east-1
      AWS_ACCESS_KEY_ID: test
      AWS_SECRET_ACCESS_KEY: test
      AWS_SQS_ENDPOINT_BASE: http://localstack:4566
      AWS_SQS_QUEUE_URL: http://localstack:4566/000000000000/tratar-ativos
    volumes:
      - ./logs/java:/var/log/myapp

  gerar-insights:
    build:
      context: ./gerar-insights
    container_name: gerar-insights
    restart: always
    depends_on:
      - localstack
    environment:
      LOCALSTACK_ENDPOINT: http://localstack:4566
      QUEUE_NAME: tratar-ativos
    volumes:
      - ./logs/python:/var/log/pyapp


  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  loki:
    image: grafana/loki:2.9.0
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:2.9.4
    container_name: promtail
    volumes:
      - ./promtail/promtail-config.yaml:/etc/promtail/config.yaml
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/log:/var/log:ro
      - /tmp:/tmp
      - /etc/machine-id:/etc/machine-id:ro
    command: -config.file=/etc/promtail/config.yaml
    depends_on:
      - loki

  gestor-insights:
    build:
      context: ./worker-insights
    container_name: gestor-insights
    restart: always
    depends_on:
      - mysql
      - worker-python-infra
    ports:
      - "8085:8085"
    environment:
      # Configurações AWS / LocalStack
      aws.region: sa-east-1
      aws.access-key: test
      aws.secret-key: test
      aws.sqs.endpoint.base: http://localstack:4566
      aws.sqs.queue.url: http://localstack:4566/000000000000/tratar-insights

      # Ajuste de porta do Spring Boot (caso necessário)
      # spring:
      #   main:
      #     web-application-type: servlet
    volumes:
      - ./logs/java:/var/log/myapp


volumes:
  mysql_data:
  localstack_data:
  grafana-data:


````


````
1  ITUB4  
2  BBDC4  
3  BPAC11  
4  ITSA4  
5  BBAS3  
6  BBDC3  
7  PETR4  
8  PETR3  
9  PRIO3  
10 VBBR3  
11 UGPA3  
12 CSAN3  
13 BRAV3  
14 VALE3  
15 AXIA3  
16 EQTL3  
17 ENEV3  
18 ELET3  
19 ENGI11  
20 B3SA3  
21 ABEV3  
22 SUZB3  
23 WEGE3  
24 CMIG4  
25 BBSE3  
26 COGN3  
27 CSNA3  
28 JBSS3  
29 BRFS3  
30 BRML3  
31 CIEL3  
32 CCRO3  
33 EMBR3  
34 RAIL3  
35 AZUL4  
36 MRFG3  
37 GGBR4  
38 SBSP3  
39 SBFG3  
40 HYPE3  
41 LREN3  
42 MGLU3  
43 TOTS3  
44 PETZ3  
45 LOGG3  
46 CVCB3  
47 OIBR3  
48 RADL3  
49 MULT3  
50 KEPL3  

````

