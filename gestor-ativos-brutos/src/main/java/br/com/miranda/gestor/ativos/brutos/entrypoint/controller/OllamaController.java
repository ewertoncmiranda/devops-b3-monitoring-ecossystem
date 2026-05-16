package br.com.miranda.gestor.ativos.brutos.entrypoint.controller;

import br.com.miranda.gestor.ativos.brutos.service.OllamaService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.Map;

import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.OLLAMA_CONTROLLER;

@Slf4j
@RestController
@RequestMapping("/ia")
public class OllamaController {

    private final OllamaService ollamaService;

    @Value("${ollama.model}")
    private String defaultModel;

    public OllamaController(OllamaService ollamaService) {
        this.ollamaService = ollamaService;
    }

    /**
     * Endpoint não-blocante para enviar um prompt ao Ollama.
     * Corpo esperado: { "prompt": "sua pergunta aqui", "model": "qwen2.5:7b" }
     * O campo "model" é opcional (padrão: valor definido em ollama.model).
     */
    @PostMapping("/prompt")
    public Mono<ResponseEntity<Map<String, String>>> enviarPrompt(@RequestBody Map<String, String> body) {
        String prompt = body.get("prompt");
        String model = body.getOrDefault("model", defaultModel);

        if (prompt == null || prompt.isBlank()) {
            log.warn("{}-Requisição recebida sem prompt", OLLAMA_CONTROLLER);
            return Mono.just(ResponseEntity.badRequest().body(Map.of("erro", "O campo 'prompt' é obrigatório")));
        }

        log.info("{}-Prompt recebido para modelo '{}': {}...", OLLAMA_CONTROLLER, model,
                prompt.substring(0, Math.min(prompt.length(), 80)));

        return ollamaService.gerarResposta(prompt, model)
                .map(resposta -> {
                    log.info("{}-Resposta gerada com sucesso. Tamanho: {} caracteres", OLLAMA_CONTROLLER, resposta.length());
                    return ResponseEntity.ok(Map.of(
                            "model", model,
                            "resposta", resposta
                    ));
                })
                .onErrorResume(e -> {
                    log.error("{}-Falha ao processar prompt: {}", OLLAMA_CONTROLLER, e.getMessage());
                    return Mono.just(ResponseEntity.internalServerError().body(Map.of(
                            "erro", "Falha na comunicação com o Ollama: " + e.getMessage()
                    )));
                });
    }
}
