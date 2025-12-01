package br.com.miranda.gestor.ativos.brutos.external.queue;

import br.com.miranda.gestor.ativos.brutos.ConfigSqs;
import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

import java.net.URI;
import java.util.logging.Logger;

@Service
public class QueueConnectImpl implements QueueConnectPort {

    @Value("${aws.sqs.endpoint.base}")
    private String sqsEndpointBase;

    @Value("${aws.sqs.queue.url}")
    private String queueUrl;

    @Autowired
    SqsClient sqsClient ;

    @Override
    public String enviarMensagemParaFila(String mensagem) {

        SendMessageResponse response = sqsClient.sendMessage(SendMessageRequest.builder()
                .queueUrl(queueUrl)
                .messageBody(mensagem)
                .build());

        return response.toString();
    }
}
