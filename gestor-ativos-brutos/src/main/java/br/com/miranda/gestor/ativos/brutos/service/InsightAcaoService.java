package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.external.InsightAcao;
import br.com.miranda.gestor.ativos.brutos.repository.InsightAcaoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class InsightAcaoService {

    private final InsightAcaoRepository repository;

    public List<InsightAcao> buscarPorSimbolo(String simbolo) {
        return repository.findBySimbolo(simbolo);
    }

    public List<InsightAcao> buscarPorSimboloNative(String simbolo) {
        return repository.findBySimboloNative(simbolo);
    }
}

