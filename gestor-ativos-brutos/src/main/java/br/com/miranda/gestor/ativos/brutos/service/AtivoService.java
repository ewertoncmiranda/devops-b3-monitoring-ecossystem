package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.external.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiAtivoDTO;
import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import br.com.miranda.gestor.ativos.brutos.tools.Utils;
import lombok.extern.slf4j.Slf4j;
import static br.com.miranda.gestor.ativos.brutos.tools.ConstantesUtils.SERVICE;
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
        log.info("{}-Iniciando processamento para ativo: {}", SERVICE, codAtivo);

        var retorno = consultaBrApiService.executar(codAtivo);

        if (Objects.isNull(retorno)) {
            log.error("{}-Resposta nula da API BRAPI para ativo: {}", SERVICE, codAtivo);
            throw new RuntimeException();
        }

        log.debug("{}-Resposta BRAPI recebida com {} resultados", SERVICE, retorno.getResults().size());

        BrapiAtivoDTO brapiDto = retorno.getResults().getFirst();
        log.debug("{}-DTO extraído: symbol={}, name={}", SERVICE, brapiDto.getSymbol(), brapiDto.getLongName());

        ModelMapper mapper = new ModelMapper();
        Ativo ativo = mapper.map(brapiDto, Ativo.class);
        log.debug("{}-Ativo mapeado para entidade de domínio: {}", SERVICE, ativo.getSymbol());

        var formatado = Utils.toJson(ativo);
        log.info("{}-Ativo convertido para JSON, tamanho: {} bytes", SERVICE, formatado.length());

        log.info("{}-Enviando mensagem para fila: {}", SERVICE, codAtivo);
        queueConnectPort.enviarMensagemParaFila(formatado);
        log.info("{}-Processamento concluído para ativo: {}", SERVICE, codAtivo);

        return ativo;
    }


}
