package br.com.miranda.gestor.ativos.brutos.external.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class OllamaResponseDTO {

    private String model;
    private String response;
    private boolean done;

    private Long totalDuration;
    private Long loadDuration;
    private Integer promptEvalCount;
    private Long promptEvalDuration;
    private Integer evalCount;
    private Long evalDuration;
}
