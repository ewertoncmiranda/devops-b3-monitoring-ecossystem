package br.com.miranda.gestor.ativos.brutos.service;

import com.google.genai.Client;
import com.google.genai.types.GenerateContentResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.GEMINI_SERVICE;

@Slf4j
@Service
public class GeminiService {

    private final Client geminiClient;
    private static final String DEFAULT_MODEL = "gemini-3-flash-preview";

    public GeminiService(Client geminiClient) {
        this.geminiClient = geminiClient;
    }

    /**
     * Gera conteúdo usando o Gemini de forma assíncrona (usando
     * Schedulers.boundedElastic pois o SDK é blocante).
     */
    public Mono<String> gerarConteudo(String prompt) {
        return gerarConteudo(prompt, DEFAULT_MODEL, null);
    }

    public Mono<String> gerarConteudo(String prompt, String model, String apiKey) {

        return Mono.fromCallable(() -> {
            Client clientToUse = geminiClient;

            if (apiKey != null && !apiKey.isBlank()) {
                clientToUse = Client.builder().apiKey(apiKey).build();
            }

            GenerateContentResponse response = clientToUse.models.generateContent(model, prompt, null);
            return response.text();
        })
                .subscribeOn(Schedulers.boundedElastic())
                .doOnSuccess(res -> log.info("{}-Conteúdo gerado com sucesso pelo Gemini", GEMINI_SERVICE))
                .doOnError(e -> log.error("{}-Erro ao gerar conteúdo no Gemini: {}", GEMINI_SERVICE, e.getMessage()));
    }
}
