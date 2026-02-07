package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;

@Slf4j
@Service
public class ConsultaBrApiService {

    @Value("${brapi.api.key}")
    private String apiKey;

    private final RestTemplate restTemplate;

    public ConsultaBrApiService() {
        this.restTemplate = new RestTemplate();
    }

    public BrapiResponseDTO executar(String symbol) {
        log.info("[BRAPI-SERVICE] Iniciando consulta para symbol: {}", symbol);

        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", apiKey);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

        HttpEntity<?> entity = new HttpEntity<>(headers);
        String url = "https://brapi.dev/api/quote/" + symbol;
        log.debug("[BRAPI-SERVICE] URL de requisição: {}", url);

        try {
            log.info("[BRAPI-SERVICE] Enviando requisição GET para BRAPI...");
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    entity,
                    String.class
            );

            log.debug("[BRAPI-SERVICE] Status HTTP recebido: {}", response.getStatusCode());
            log.debug("[BRAPI-SERVICE] Tamanho da resposta: {} bytes", response.getBody().length());

            ObjectMapper mapper = new ObjectMapper();
            BrapiResponseDTO result = mapper.readValue(response.getBody(), BrapiResponseDTO.class);

            log.info("[BRAPI-SERVICE] Resposta parseada com sucesso. , Resultados: {}",
                  result.getResults().size());

            return result;

        } catch (HttpClientErrorException.NotFound ex) {
            log.warn("[BRAPI-SERVICE] Ativo não encontrado: {} (404)", symbol);
            return null;
        } catch (HttpClientErrorException ex) {
            log.error("[BRAPI-SERVICE] Erro HTTP ao consultar Brapi. Symbol: {}, Status: {}, Mensagem: {}",
                    symbol, ex.getStatusCode(), ex.getMessage());
            throw ex;
        } catch (JsonProcessingException e) {
            log.error("[BRAPI-SERVICE] Erro ao processar JSON da resposta BRAPI. Symbol: {}", symbol, e);
            throw new RuntimeException("Erro ao processar JSON da resposta da Brapi", e);
        }
    }
}
