package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.external.dto.OllamaRequestDTO;
import br.com.miranda.gestor.ativos.brutos.external.dto.OllamaResponseDTO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.Map;

import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.OLLAMA_SERVICE;

@Slf4j
@Service
public class OllamaService {

    private final WebClient ollamaWebClient;

    @Value("${ollama.model}")
    private String defaultModel;

    @Value("${ollama.system-prompt}")
    private String systemPrompt;

    @Value("${ollama.max-tokens}")
    private int maxTokens;

    @Value("${ollama.temperature}")
    private double temperature;

    @Value("${ollama.context-length}")
    private int contextLength;

    public OllamaService(WebClient ollamaWebClient) {
        this.ollamaWebClient = ollamaWebClient;
    }

    /**
     * Envia um prompt usando o modelo e configurações padrão definidos no properties.
     */
    public Mono<String> gerarResposta(String prompt) {
        return gerarResposta(prompt, defaultModel);
    }

    /**
     * Envia um prompt para um modelo específico com as configurações de tokens, temperatura e contexto.
     */
    public Mono<String> gerarResposta(String prompt, String model) {
        log.info("{}-Enviando prompt para modelo '{}'. Tamanho: {} chars | Max tokens: {} | Temp: {} | Ctx: {}",
                OLLAMA_SERVICE, model, prompt.length(), maxTokens, temperature, contextLength);

        OllamaRequestDTO request = OllamaRequestDTO.builder()
                .model(model)
                .prompt(prompt)
                .system(systemPrompt)
                .stream(false)
                .options(Map.of(
                        "temperature", temperature,
                        "num_predict", maxTokens,
                        "num_ctx", contextLength
                ))
                .build();

        return ollamaWebClient.post()
                .uri("/api/generate")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(OllamaResponseDTO.class)
                .map(body -> {
                    log.info("{}-Resposta recebida do modelo '{}'. Tokens gerados: {}",
                            OLLAMA_SERVICE, body.getModel(), body.getEvalCount());
                    return body.getResponse();
                })
                .doOnError(e -> log.error("{}-Erro ao comunicar com Ollama: {}", OLLAMA_SERVICE, e.getMessage(), e));
    }
}
