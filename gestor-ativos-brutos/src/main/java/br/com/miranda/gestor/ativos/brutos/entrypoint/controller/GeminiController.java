package br.com.miranda.gestor.ativos.brutos.entrypoint.controller;

import br.com.miranda.gestor.ativos.brutos.service.GeminiService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import java.util.Map;

import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.GEMINI_CONTROLLER;

@Slf4j
@RestController
@RequestMapping("/gemini")
public class GeminiController {

    private final GeminiService geminiService;

    public GeminiController(GeminiService geminiService) {
        this.geminiService = geminiService;
    }

    @PostMapping("/prompt")
    public Mono<ResponseEntity<Map<String, String>>> enviarPrompt(@RequestBody Map<String, String> body) {
        String prompt = body.get("prompt");
        String model = body.getOrDefault("model", "gemini-3-flash-preview");

        if (prompt == null || prompt.isBlank()) {
            return Mono.just(ResponseEntity.badRequest().body(Map.of("erro", "O campo 'prompt' é obrigatório")));
        }

        log.info("{}-Requisição recebida para Gemini. Modelo: {}", GEMINI_CONTROLLER, model);

        return geminiService.gerarConteudo(prompt, model)
                .map(resposta -> ResponseEntity.ok(Map.of(
                        "model", model,
                        "resposta", resposta
                )))
                .onErrorResume(e -> Mono.just(ResponseEntity.internalServerError().body(Map.of(
                        "erro", "Falha ao processar no Gemini: " + e.getMessage()
                ))));
    }
}
