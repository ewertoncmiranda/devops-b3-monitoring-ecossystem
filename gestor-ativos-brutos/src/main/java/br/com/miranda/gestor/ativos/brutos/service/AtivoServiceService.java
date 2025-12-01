package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.tools.Utils;
import br.com.miranda.gestor.ativos.brutos.external.database.entidade.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiAtivoDTO;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;
import br.com.miranda.gestor.ativos.brutos.external.database.repository.AtivoRepository;
import br.com.miranda.gestor.ativos.brutos.port.AtivoServicePort;
import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class AtivoServiceService implements AtivoServicePort {

    private final ConsultaBrApiService consultaBrApiService;
    private final AtivoRepository ativoRepository;

    private final QueueConnectPort queueConnectPort;

    public AtivoServiceService(ConsultaBrApiService consultaBrApiService, AtivoRepository ativoRepository, QueueConnectPort port) {
        this.consultaBrApiService = consultaBrApiService;
        this.ativoRepository = ativoRepository;
        this.queueConnectPort = port;
    }


    @Override
    public Ativo salvar(String codAtivo) {

        var retorno = buscarPorSymbol(codAtivo);

        if (Objects.isNull(retorno)) {
            //TODO CRIAR EXCEPTION CONTEXTUALIZADA
            throw new RuntimeException();
        }
        BrapiAtivoDTO brapiDto = retorno.getResults().getFirst();
        ModelMapper mapper = new ModelMapper();
        Ativo ativo = mapper.map(brapiDto, Ativo.class);
        var ativoSalvo = ativoRepository.save(ativo);
        var formatado = Utils.toJson(ativoSalvo);
        queueConnectPort.enviarMensagemParaFila(formatado);
        return ativoSalvo;

    }

    @Override
    public BrapiResponseDTO buscarPorSymbol(String symbol) {
        return consultaBrApiService.executar(symbol);
    }


}
