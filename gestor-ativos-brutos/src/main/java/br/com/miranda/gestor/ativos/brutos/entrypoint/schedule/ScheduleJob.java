package br.com.miranda.gestor.ativos.brutos.entrypoint.schedule;

import br.com.miranda.gestor.ativos.brutos.service.AtivoService;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;

import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.SCHEDULER ;

@Slf4j
@Component
@EnableScheduling
@AllArgsConstructor
public class ScheduleJob {

    private final AtivoService servicePort;

    // fila thread-safe para armazenar códigos registrados via endpoint
    private final ConcurrentLinkedQueue<String> queue = new ConcurrentLinkedQueue<>();

    /**
     * Método chamado por controlador/serviço para registrar um código para processamento assíncrono.
     */
    public void registerAtivo(String codigoAtivo) {
        if (codigoAtivo == null || codigoAtivo.isBlank()) {
            return;
        }
        queue.add(codigoAtivo.trim().toUpperCase());
        log.debug("{}-Ativo registrado na fila: {}", SCHEDULER, codigoAtivo);
    }


    @Scheduled(fixedDelay = 25000)
    public void processarAcoes() {
        log.info("{}-Iniciando processamento em lote de ações", SCHEDULER);

        List<String> acoes = new ArrayList<>();
        String codigo;
        while ((codigo = queue.poll()) != null) {
            acoes.add(codigo);
        }

        if (acoes.isEmpty()) {
            log.debug("{}-Nenhuma ação na fila de registro. Nenhuma ação processada neste ciclo.", SCHEDULER);
            return;
        }

        log.info("{}-Total de ações a processar: {}", SCHEDULER, acoes.size());

        for (String codigoAcao : acoes) {
            log.info("{}-Processando ação: {}", SCHEDULER, codigoAcao);
            try {
                servicePort.processar(codigoAcao);
                log.info("{}-Ação processada com sucesso: {}", SCHEDULER, codigoAcao);
            } catch (Exception e) {
                log.error("{}-Erro ao processar ação: {}. Erro: {}", SCHEDULER, codigoAcao, e.getMessage(), e);
            }
        }

        log.info("{}-Processamento em lote concluído", SCHEDULER);
    }

}

