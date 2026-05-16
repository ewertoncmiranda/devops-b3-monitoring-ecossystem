package br.com.miranda.gestor.ativos.brutos.external.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class OllamaRequestDTO {

    private String model;
    private String prompt;
    private String system;

    @Builder.Default
    private boolean stream = false;

    /**
     * Opções de geração do modelo (temperature, num_predict, num_ctx, etc.)
     */
    private Map<String, Object> options;
}
