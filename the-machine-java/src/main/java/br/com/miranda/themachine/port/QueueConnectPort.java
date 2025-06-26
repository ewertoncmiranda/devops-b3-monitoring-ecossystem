package br.com.miranda.themachine.port;

public interface QueueConnectPort {
    String enviarMensagemParaFila(String mensagem);
}
