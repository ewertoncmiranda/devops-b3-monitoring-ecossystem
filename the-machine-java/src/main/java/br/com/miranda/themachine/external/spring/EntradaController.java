package br.com.miranda.themachine.external.spring;

import br.com.miranda.themachine.entidade.PersonagemEntity;
import br.com.miranda.themachine.port.PersonagemServicePort;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/app")
public class EntradaController {

    @Autowired
    PersonagemServicePort portPesonagens ;



    @GetMapping
    public ResponseEntity<String> ola(){
        return ResponseEntity.ok("Seja Bem-vindo !");
    }

    @PostMapping("/create")
    public ResponseEntity<?> criarRegistroTabela(){
        PersonagemEntity random = portPesonagens.random();
        return ResponseEntity.ok(random);
    }
}
