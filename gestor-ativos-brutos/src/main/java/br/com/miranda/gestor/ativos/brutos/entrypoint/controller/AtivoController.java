package br.com.miranda.gestor.ativos.brutos.entrypoint.controller;


import br.com.miranda.gestor.ativos.brutos.external.Ativo;
import br.com.miranda.gestor.ativos.brutos.service.AtivoService;
import lombok.extern.slf4j.Slf4j;
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
        log.info("[CONTROLLER] Requisição recebida para buscar ativo: {}", ativo);
        var ativo1 = service.processar(ativo);
        log.info("[CONTROLLER] Resposta preparada para ativo: {}", ativo);
        return ativo != null ? ResponseEntity.ok(ativo1) : ResponseEntity.notFound().build();
    }

}

