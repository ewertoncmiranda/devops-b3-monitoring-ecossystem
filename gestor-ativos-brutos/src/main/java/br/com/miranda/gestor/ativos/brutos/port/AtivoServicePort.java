package br.com.miranda.gestor.ativos.brutos.port;

import br.com.miranda.gestor.ativos.brutos.entidade.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;

import java.util.List;

public interface AtivoServicePort {
    Ativo salvar(String ativo);
    BrapiResponseDTO buscarPorSymbol(String symbol);

}
