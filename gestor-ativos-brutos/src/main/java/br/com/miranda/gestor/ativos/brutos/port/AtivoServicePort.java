package br.com.miranda.gestor.ativos.brutos.port;

import br.com.miranda.gestor.ativos.brutos.external.database.entidade.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;

public interface AtivoServicePort {
    Ativo salvar(String ativo);
    BrapiResponseDTO buscarPorSymbol(String symbol);

}
