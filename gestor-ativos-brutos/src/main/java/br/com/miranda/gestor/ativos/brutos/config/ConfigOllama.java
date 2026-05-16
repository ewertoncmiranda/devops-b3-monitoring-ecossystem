package br.com.miranda.gestor.ativos.brutos.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;

@Slf4j
@Configuration
public class ConfigOllama {

    @Value("${ollama.endpoint}")
    private String ollamaEndpoint;

    @Bean
    public WebClient ollamaWebClient() {
        log.info("(CONFIG-OLLAMA)-Inicializando WebClient reativo para Ollama com endpoint: {}", ollamaEndpoint);

        HttpClient httpClient = HttpClient.create()
                .responseTimeout(Duration.ofMinutes(30));

        return WebClient.builder()
                .baseUrl(ollamaEndpoint)
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .build();
    }
}
