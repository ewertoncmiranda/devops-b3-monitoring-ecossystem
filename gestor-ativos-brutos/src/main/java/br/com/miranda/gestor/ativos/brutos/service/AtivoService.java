package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.external.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiAtivoDTO;
import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import br.com.miranda.gestor.ativos.brutos.tools.Utils;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Slf4j
@Service
public class AtivoService {

    private final ConsultaBrApiService consultaBrApiService;
    private final QueueConnectPort queueConnectPort;

    public AtivoService(ConsultaBrApiService consultaBrApiService, QueueConnectPort port) {
        this.consultaBrApiService = consultaBrApiService;
        this.queueConnectPort = port;
    }


    public Ativo processar(String codAtivo) {
        log.info("[SERVICE] Iniciando processamento para ativo: {}", codAtivo);

        var retorno = consultaBrApiService.executar(codAtivo);

        if (Objects.isNull(retorno)) {
            log.error("[SERVICE] Resposta nula da API BRAPI para ativo: {}", codAtivo);
            throw new RuntimeException();
        }

        log.debug("[SERVICE] Resposta BRAPI recebida com {} resultados", retorno.getResults().size());

        BrapiAtivoDTO brapiDto = retorno.getResults().getFirst();
        log.debug("[SERVICE] DTO extraído: symbol={}, name={}", brapiDto.getSymbol(), brapiDto.getLongName());

        ModelMapper mapper = new ModelMapper();
        Ativo ativo = mapper.map(brapiDto, Ativo.class);
        log.debug("[SERVICE] Ativo mapeado para entidade de domínio: {}", ativo.getSymbol());

        var formatado = Utils.toJson(ativo);
        log.info("[SERVICE] Ativo convertido para JSON, tamanho: {} bytes", formatado.length());

        log.info("[SERVICE] Enviando mensagem para fila: {}", codAtivo);
        queueConnectPort.enviarMensagemParaFila(formatado);
        log.info("[SERVICE] Processamento concluído para ativo: {}", codAtivo);

        return ativo;
    }


}
