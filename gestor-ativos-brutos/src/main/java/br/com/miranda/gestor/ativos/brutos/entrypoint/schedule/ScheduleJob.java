package br.com.miranda.gestor.ativos.brutos.entrypoint.schedule;
import br.com.miranda.gestor.ativos.brutos.port.AtivoServicePort;
import lombok.AllArgsConstructor;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@EnableScheduling
@AllArgsConstructor
public class ScheduleJob {

    AtivoServicePort servicePort;

    @Scheduled(fixedDelay = 25000)
    public void processarAcoes() {

        List<String> acoes = acoesPrincipais;

        for (String codigo : acoes) {

            System.out.print("Processando a ação : " + codigo + " \n");
            servicePort.salvar(codigo);


        }
    }

    public static List<String> acoesPrincipais = List.of(
            "VALE3", "PETR4", "PETR3", "ITUB4", "BBAS3" ) ; /*"BBDC4", "BBDC3", "ITSA4",
            "SUZB3", "WEGE3", "RENT3", "JBSS3", "ABEV3", "B3SA3", "PRIO3", "EQTL3",
            "ENEV3", "ELET3", "GGBR4", "CSNA3", "CMIG4", "CPLE6", "TAEE11", "VIVT3",
            "RAIL3", "CCRO3", "SBSP3", "BRFS3", "HYPE3", "LREN3", "MGLU3", "AMER3",
            "ARCZ3", "ARZZ3", "EZTC3", "CYRE3", "MRVE3", "CVCB3", "MULT3", "BRML3",
            "BEEF3", "GOAU4", "CRFB3", "PCAR3", "ENBR3", "ALPA4", "FLRY3", "RADL3",
            "BRKM5", "KLBN11", "EMBR3", "BRAP4", "CPFE3", "COGN3", "TIMS3", "BPAC11",
            "SANB11", "GMAT3", "USIM5", "USIM3", "CSMG3", "PETZ3", "AMBP3", "POSI3",
            "MLAS3", "NGRD3", "NTCO3", "LWSA3", "BIDI11", "BIDI4", "BIDI3", "VIIA3",
            "SOMA3", "GRND3", "RRRP3", "DXCO3", "AESB3", "SLCE3", "SMTO3", "TOTS3",
            "BRIT3", "ORVR3", "QUAL3", "SEQL3", "YDUQ3", "SULA11", "SULA4", "SULA3",
            "LIGT3", "ENGI11", "FESA4", "MRFG3", "CPLE3", "TRPL4", "ALUP11", "MDIA3",
            "GUAR3", "LOGG3", "TGMA3", "POMO4", "MOVI3", "LEVE3", "PLPL3", "CURY3 ); */


}

