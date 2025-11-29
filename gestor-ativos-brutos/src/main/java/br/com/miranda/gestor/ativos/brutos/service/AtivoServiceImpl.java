package br.com.miranda.gestor.ativos.brutos.service;

import br.com.miranda.gestor.ativos.brutos.Utils;
import br.com.miranda.gestor.ativos.brutos.entidade.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiAtivoDTO;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiResponseDTO;
import br.com.miranda.gestor.ativos.brutos.external.repository.AtivoRepository;
import br.com.miranda.gestor.ativos.brutos.entrypoint.spring.external.ConsultaBrapiExternal;
import br.com.miranda.gestor.ativos.brutos.port.AtivoServicePort;
import br.com.miranda.gestor.ativos.brutos.port.QueueConnectPort;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.util.Objects;

@Service
public class AtivoServiceImpl implements AtivoServicePort {

    private final ConsultaBrapiExternal consultaBrapiExternal;
    private final AtivoRepository ativoRepository;

    private final QueueConnectPort queueConnectPort;

    public AtivoServiceImpl(ConsultaBrapiExternal consultaBrapiExternal, AtivoRepository ativoRepository, QueueConnectPort port) {
        this.consultaBrapiExternal = consultaBrapiExternal;
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
        BrapiAtivoDTO brapiDto = retorno.getResults().get(0);
        ModelMapper mapper = new ModelMapper();
        Ativo ativo = mapper.map(brapiDto, Ativo.class);
        var ativoSalvo = ativoRepository.save(ativo);
        var formatado = Utils.toJson(ativoSalvo);
        queueConnectPort.enviarMensagemParaFila(formatado);
        return ativoSalvo;

    }

    @Override
    public BrapiResponseDTO buscarPorSymbol(String symbol) {
        return consultaBrapiExternal.executar(symbol);
    }


}
