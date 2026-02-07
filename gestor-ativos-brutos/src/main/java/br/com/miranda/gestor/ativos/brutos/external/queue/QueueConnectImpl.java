package br.com.miranda.gestor.ativos.brutos.external.queue;

import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import lombok.extern.slf4j.Slf4j;
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
        log.info("[QUEUE] Preparando envio de mensagem para fila: {}", queueUrl);
        log.debug("[QUEUE] Tamanho da mensagem: {} bytes", mensagem.length());
        log.debug("[QUEUE] Conteúdo da mensagem: {}", mensagem.substring(0, Math.min(200, mensagem.length())) + "...");

        try {
            SendMessageResponse response = sqsClient.sendMessage(SendMessageRequest.builder()
                    .queueUrl(queueUrl)
                    .messageBody(mensagem)
                    .build());

            log.info("[QUEUE] Mensagem enviada com sucesso. Message ID: {}", response.messageId());
            log.debug("[QUEUE] Resposta SQS: {}", response.toString());

            return response.toString();
        } catch (Exception e) {
            log.error("[QUEUE] Erro ao enviar mensagem para fila: {}. Erro: {}", queueUrl, e.getMessage(), e);
            throw e;
        }
    }
}
