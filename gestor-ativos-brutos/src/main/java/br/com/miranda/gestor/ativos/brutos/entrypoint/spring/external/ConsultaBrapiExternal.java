package br.com.miranda.gestor.ativos.brutos.entrypoint.spring.external;

import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;

@Service
public class ConsultaBrapiExternal {

    private static final String API_KEY = "kJfyqy8yUVj94SivLsKq4Q";
    private final RestTemplate restTemplate;

    public ConsultaBrapiExternal() {
        this.restTemplate = new RestTemplate();
    }

    public BrapiResponseDTO executar(String symbol) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", API_KEY);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

        HttpEntity<?> entity = new HttpEntity<>(headers);
        String url = "https://brapi.dev/api/quote/" + symbol;

        try {
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    entity,
                    String.class
            );

            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(response.getBody(), BrapiResponseDTO.class);

        } catch (HttpClientErrorException.NotFound ex) {
            System.out.println("Ativo não encontrado: " + symbol);
            return null;
        } catch (HttpClientErrorException ex) {
            System.out.println("Erro HTTP ao consultar Brapi: " + ex.getStatusCode());
            throw ex;
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Erro ao processar JSON da resposta da Brapi", e);
        }
    }
}
