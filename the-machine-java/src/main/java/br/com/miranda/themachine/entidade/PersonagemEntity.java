package br.com.miranda.themachine.entidade;

import br.com.miranda.themachine.PersonagemDTO;
import jakarta.persistence.*;

@Entity
@Table(name = "personagem")
public class PersonagemEntity {

    public PersonagemEntity() {}

    public PersonagemEntity(PersonagemDTO dto) {
        this.nome = dto.getNome();
        this.vida = dto.getVida();
        this.forca = dto.getForca();
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nome;
    private int forca;
    private int vida;

    // Getters e Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public int getVida() {
        return vida;
    }

    public void setVida(int vida) {
        this.vida = vida;
    }

    public int getForca() {
        return forca;
    }

    public void setForca(int forca) {
        this.forca = forca;
    }
}
