package br.com.miranda.gestor.ativos.brutos.tools;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Utils {

    public static String toJson(Object obj) {
        try {
            log.debug("[UTILS] Iniciando conversão para JSON. Tipo: {}", obj.getClass().getSimpleName());

            ObjectMapper mapper = new ObjectMapper();
            String json = mapper.writeValueAsString(obj);

            log.debug("[UTILS] JSON gerado com sucesso. Tamanho: {} bytes", json.length());

            return json;
        } catch (Exception e) {
            log.error("[UTILS] Erro ao converter objeto para JSON. Tipo: {}, Erro: {}",
                    obj.getClass().getSimpleName(), e.getMessage(), e);
            throw new RuntimeException("Erro ao converter objeto para JSON", e);
        }
    }


}
