package br.com.miranda.gestor.ativos.brutos.entrypoint.spring.controller;


import br.com.miranda.gestor.ativos.brutos.entidade.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;
import br.com.miranda.gestor.ativos.brutos.port.AtivoServicePort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Objects;

@RestController
@RequestMapping("/ativos")
public class AtivoController {

    private final AtivoServicePort service;

    public AtivoController(AtivoServicePort service) {
        this.service = service;
    }

    @GetMapping("/{ativo}")
    public ResponseEntity<BrapiResponseDTO> buscarPorSymbol(@PathVariable String ativo) {
        BrapiResponseDTO ativo1 = service.buscarPorSymbol(ativo);
        return ativo != null ? ResponseEntity.ok(ativo1) : ResponseEntity.notFound().build();
    }

    @PostMapping
    public  ResponseEntity<Ativo> cadastrarNovoAtivo(@RequestBody String ativo){
        Ativo save = service.salvar(ativo);
        return ResponseEntity.ok(save);
    }

}

