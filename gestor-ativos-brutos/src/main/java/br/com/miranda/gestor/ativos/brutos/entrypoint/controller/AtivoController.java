package br.com.miranda.gestor.ativos.brutos.entrypoint.controller;


import br.com.miranda.gestor.ativos.brutos.external.Ativo;
import br.com.miranda.gestor.ativos.brutos.service.AtivoService;
import lombok.extern.slf4j.Slf4j;
import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.CONTROLLER;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/ativos")
public class AtivoController {

    private final AtivoService service;

    public AtivoController(AtivoService service) {
        this.service = service;
    }

    @GetMapping("/{ativo}")
    public ResponseEntity<Ativo> buscarPorSymbol(@PathVariable String ativo) {
        log.info("{}-Requisição recebida para buscar ativo: {}", CONTROLLER, ativo);
        var ativo1 = service.processar(ativo);
        log.info("{}-Resposta preparada para ativo: {}", CONTROLLER, ativo);
        return ativo != null ? ResponseEntity.ok(ativo1) : ResponseEntity.notFound().build();
    }

}

