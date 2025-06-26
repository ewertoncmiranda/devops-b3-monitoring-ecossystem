package br.com.miranda.themachine.external.spring;

import br.com.miranda.themachine.port.QueueConnectPort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/fila")
public class QueueController {

    public QueueController(QueueConnectPort port) {
        this.port = port;
    }

    QueueConnectPort port ;

    @GetMapping
    public ResponseEntity<?> estimulaFila(@RequestBody String mensagem){
        String o = port.enviarMensagemParaFila(mensagem);
        return ResponseEntity.ok(o);
    }
}
