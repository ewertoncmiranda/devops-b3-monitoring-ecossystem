package br.com.miranda.gestor.ativos.brutos;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Utils {


    public static String toJson(Object obj) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            return mapper.writeValueAsString(obj);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao converter objeto para JSON", e);
        }
    }


}
