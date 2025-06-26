package br.com.miranda.themachine.external.queue;

import br.com.miranda.themachine.port.QueueConnectPort;
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

    @Override
    public String enviarMensagemParaFila(String mensagem) {
        SqsClient sqsClient = SqsClient.builder()
                .endpointOverride(URI.create(sqsEndpointBase))
                .region(Region.SA_EAST_1)
                .credentialsProvider(StaticCredentialsProvider.create(
                        AwsBasicCredentials.create("test", "test")))
                .build();

        Logger log = Logger.getLogger("the-machine:");
        log.info(queueUrl);
        log.info(sqsEndpointBase);

        SendMessageResponse response = sqsClient.sendMessage(SendMessageRequest.builder()
                .queueUrl(queueUrl)
                .messageBody(mensagem)
                .build());

        return response.toString();
    }
}
