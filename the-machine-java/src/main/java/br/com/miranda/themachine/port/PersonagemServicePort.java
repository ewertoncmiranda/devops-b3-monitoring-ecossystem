package br.com.miranda.themachine.port;

import br.com.miranda.themachine.PersonagemDTO;
import br.com.miranda.themachine.entidade.PersonagemEntity;

import java.util.List;

public interface PersonagemServicePort {
    PersonagemEntity criar(PersonagemDTO dto);

    PersonagemEntity atualizar(Long id, PersonagemDTO dto);

    void deletar(Long id);

    PersonagemEntity buscarPorId(Long id);

    List<PersonagemEntity> listarTodos();

    PersonagemEntity random();
}
