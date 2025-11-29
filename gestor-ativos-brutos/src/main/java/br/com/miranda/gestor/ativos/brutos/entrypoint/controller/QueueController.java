package br.com.miranda.gestor.ativos.brutos.entrypoint.controller;

import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import org.apache.logging.log4j.util.Strings;
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
        System.out.print(Strings.concat("Entrada da fila : ",mensagem) );
        String o = port.enviarMensagemParaFila(mensagem);
        return ResponseEntity.ok(o);
    }
}
