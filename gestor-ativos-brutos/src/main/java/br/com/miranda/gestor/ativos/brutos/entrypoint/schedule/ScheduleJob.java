package br.com.miranda.gestor.ativos.brutos.entrypoint.schedule;
import br.com.miranda.gestor.ativos.brutos.service.AtivoService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Slf4j
@Component
@EnableScheduling
@AllArgsConstructor
public class ScheduleJob {

    AtivoService servicePort;

    @Scheduled(fixedDelay = 25000)
    public void processarAcoes() {
        log.info("[SCHEDULER] Iniciando processamento em lote de ações");

        List<String> acoes = acoesPrincipais;
        log.info("[SCHEDULER] Total de ações a processar: {}", acoes.size());

        for (String codigo : acoes) {
            log.info("[SCHEDULER] Processando ação: {}", codigo);
            try {
                servicePort.processar(codigo);
                log.info("[SCHEDULER] Ação processada com sucesso: {}", codigo);
            } catch (Exception e) {
                log.error("[SCHEDULER] Erro ao processar ação: {}. Erro: {}", codigo, e.getMessage(), e);
            }
        }

        log.info("[SCHEDULER] Processamento em lote concluído");
    }

    public static List<String> acoesPrincipais = List.of(
            "VALE3", "PETR4", "PETR3", "ITUB4", "BBAS3" ) ;

}

