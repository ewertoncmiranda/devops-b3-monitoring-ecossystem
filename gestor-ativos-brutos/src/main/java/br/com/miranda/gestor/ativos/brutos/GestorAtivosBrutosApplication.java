package br.com.miranda.gestor.ativos.brutos;

import br.com.miranda.gestor.ativos.brutos.config.DatabaseHealthCheck;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.context.event.EventListener;

import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.MAIN;

@Slf4j
@SpringBootApplication
@RequiredArgsConstructor
public class GestorAtivosBrutosApplication {

    private final DatabaseHealthCheck databaseHealthCheck;

    public static void main(String[] args) {
        log.info("{} ========================================", MAIN);
        log.info("{} Iniciando aplicação: GestorAtivosBrutosApplication", MAIN);
        log.info("{} ========================================", MAIN);

        SpringApplication.run(GestorAtivosBrutosApplication.class, args);

        log.info("{} ========================================", MAIN);
        log.info("{} Aplicação iniciada com sucesso!", MAIN);
        log.info("{} ========================================", MAIN);
    }

    @EventListener(ContextRefreshedEvent.class)
    public void onApplicationStart() {
        boolean dbAvailable = databaseHealthCheck.isDatabaseAvailable();
        if (dbAvailable) {
            log.info("(STARTUP)-Aplicação iniciada com sucesso. Banco de dados disponível.");
        } else {
            log.warn("(STARTUP)-Aplicação iniciada, mas banco de dados NÃO está disponível. "
                    + "Operações que exigem DB falharão com DatabaseUnavailableException.");
        }
    }
}
