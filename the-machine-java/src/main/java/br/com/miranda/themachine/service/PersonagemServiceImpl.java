package br.com.miranda.themachine.service;

import br.com.miranda.themachine.PersonagemDTO;
import br.com.miranda.themachine.entidade.PersonagemEntity;
import br.com.miranda.themachine.port.PersonagemServicePort;
import br.com.miranda.themachine.external.repository.PersonagemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PersonagemServiceImpl implements PersonagemServicePort {

    @Autowired
    private PersonagemRepository repository;

    @Override
    public PersonagemEntity criar(PersonagemDTO dto) {
        PersonagemEntity p = new PersonagemEntity(dto);
        return repository.save(p);
    }

    @Override
    public PersonagemEntity atualizar(Long id, PersonagemDTO dto) {
        PersonagemEntity existente = repository.findById(id).orElseThrow();
        existente.setNome(dto.getNome());
        existente.setForca(dto.getForca());
        existente.setVida(dto.getVida());
        return repository.save(existente);
    }

    @Override
    public void deletar(Long id) {
        repository.deleteById(id);
    }

    @Override
    public PersonagemEntity buscarPorId(Long id) {
        return repository.findById(id).orElseThrow();
    }

    @Override
    public List<PersonagemEntity> listarTodos() {
        return repository.findAll();
    }

    @Override
    public PersonagemEntity random() {
        var personagem = new PersonagemEntity();
        personagem.setForca(2);
        personagem.setVida(5);
        personagem.setNome("Magician");
        PersonagemEntity save = repository.save(personagem);
        return save ;
    }
}
