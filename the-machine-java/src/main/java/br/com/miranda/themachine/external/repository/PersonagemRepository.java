package br.com.miranda.themachine.external.repository;

import br.com.miranda.themachine.entidade.PersonagemEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PersonagemRepository extends JpaRepository<PersonagemEntity, Long> {
}