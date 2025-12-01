package br.com.miranda.gestor.ativos.brutos.external.database.repository;


import br.com.miranda.gestor.ativos.brutos.external.database.entidade.Ativo;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AtivoRepository extends JpaRepository<Ativo, Long> {
    Ativo findBySymbol(String symbol);
}
