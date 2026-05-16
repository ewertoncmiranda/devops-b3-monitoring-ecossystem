package br.com.miranda.gestor.ativos.brutos.entrypoint.schedule;
import br.com.miranda.gestor.ativos.brutos.service.AtivoService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;
import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.SCHEDULER ;
@Slf4j
@Component
@EnableScheduling
@AllArgsConstructor
public class ScheduleJob {

    AtivoService servicePort;

    @Scheduled(fixedDelay = 25000)
    public void processarAcoes() {
        log.info("{}-Iniciando processamento em lote de ações",SCHEDULER);

        List<String> acoes = acoesPrincipais;
        log.info("{}-Total de ações a processar: {}",SCHEDULER, acoes.size());;

        for (String codigo : acoes) {
            log.info("{}-Processando ação: {}",SCHEDULER, codigo);
            try {
                servicePort.processar(codigo);
                log.info("{}-Ação processada com sucesso: {}",SCHEDULER, codigo);
            } catch (Exception e) {
                log.error("{}-Erro ao processar ação: {}. Erro: {}",SCHEDULER, codigo, e.getMessage(), e);
            }
        }

        log.info("{}-Processamento em lote concluído",SCHEDULER);
    }

    public static List<String> acoesPrincipais = List.of(
            "VALE3", "PETR4", "PETR3", "ITUB4", "BBAS3" ) ;

}

