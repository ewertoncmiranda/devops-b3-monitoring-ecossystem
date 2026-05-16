package br.com.miranda.gestor.ativos.brutos.external.queue;

import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import lombok.extern.slf4j.Slf4j;
import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.QUEUE;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

@Slf4j
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
        log.info("{}-Preparando envio de mensagem para fila: {}", QUEUE, queueUrl);
        log.debug("{}-Conteúdo da mensagem: {}", QUEUE, mensagem.substring(0, Math.min(200, mensagem.length())) + "...");

        try {
            SendMessageResponse response = sqsClient.sendMessage(SendMessageRequest.builder()
                    .queueUrl(queueUrl)
                    .messageBody(mensagem)
                    .build());

            log.info("{}-Mensagem enviada com sucesso. Message ID: {}", QUEUE, response.messageId());
            log.debug("{}-Resposta SQS: {}", QUEUE, response.toString());

            return response.toString();
        } catch (Exception e) {
            log.error("{}-Erro ao enviar mensagem para fila: {}. Erro: {}", QUEUE, queueUrl, e.getMessage(), e);
            throw e;
        }
    }
}
