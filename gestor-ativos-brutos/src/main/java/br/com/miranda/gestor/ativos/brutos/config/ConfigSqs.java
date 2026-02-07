package br.com.miranda.gestor.ativos.brutos.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;

import java.net.URI;

@Slf4j
@Configuration
public class ConfigSqs {

    @Value("${aws.sqs.endpoint.base}")
    private String sqsEndpointBase;

    @Bean
    public SqsClient config() {
        log.info("[CONFIG-SQS] Inicializando SqsClient com endpoint: {}", sqsEndpointBase);
        log.info("[CONFIG-SQS] Região configurada: SA_EAST_1");

        SqsClient sqsClient = SqsClient.builder()
                .endpointOverride(URI.create(sqsEndpointBase))
                .region(Region.SA_EAST_1)
                .credentialsProvider(StaticCredentialsProvider.create(
                        AwsBasicCredentials.create("test", "test")))
                .build();

        log.info("[CONFIG-SQS] SqsClient criado com sucesso");
        return sqsClient;
    }
}
