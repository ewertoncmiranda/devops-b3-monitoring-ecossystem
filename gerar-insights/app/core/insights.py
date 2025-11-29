def gerar_insights(ativo):
    preco = ativo["regularMarketPrice"]
    pl = ativo["priceEarnings"]
    lpa = ativo["earningsPerShare"]
    abertura = ativo["regularMarketOpen"]
    fechamento = ativo["regularMarketPreviousClose"]
    max52 = ativo["fiftyTwoWeekHigh"]
    min52 = ativo["fiftyTwoWeekLow"]
    market_cap = ativo["marketCap"]
    volume = ativo["regularMarketVolume"]
    max_dia = ativo["regularMarketDayHigh"]
    min_dia = ativo["regularMarketDayLow"]
    crescimento_estimado = 10  # estimativa padrão

    return {
        # 🧠 Fundamentalistas
        "PL_barato": pl < 12,
        "PEG_barato": (pl / crescimento_estimado) < 1,
        "EarningsYield_>Tesouro": ((lpa / preco) * 100) > 11.5,
        "Desconto_>20%_Max52": ((max52 - preco) / max52 * 100) > 20,
        ">10%_da_Min52": ((preco - min52) / min52 * 100) > 10,
        "Lucro/MarketCap_>5%": (lpa * 1e9 / market_cap) > 0.05,
        "<ValorGraham": preco < lpa * (8.5 + 2 * crescimento_estimado),
        "<PrecoJustoSetor": preco < lpa * 15,

        # 📈 Técnicos
        "Oscilacao_Dia_%": (max_dia - min_dia) / abertura * 100,
        "Candle_Doji": abertura == fechamento,
        "Martelo": (min_dia < abertura - 0.5) and (fechamento > abertura),
        "Volume_Forte?": "Indeterminado (histórico necessário)",
        "Subindo": ativo["regularMarketChange"] > 0 and preco > abertura,

        # 📊 Relativos e Momentum
        "Forca_Relativa_%": (preco - min52) / (max52 - min52) * 100,
        "ReversaoMedia": "Indeterminado (MM20 necessária)",
        "Perto_Resistencia": preco >= max52 * 0.95,

        # 📚 Acadêmicos e Quant
        "Fama_French_Valor": pl < 10,
        "CAPM_Retorno_Esperado_%": 11.5 + 1.2 * (15 - 11.5),
        "Sharpe_Like": (((lpa / preco) * 100) - 11.5) / 5,  # vol. estimada
        "Filtro_Graham": pl < 15,
        "Peter_Lynch_OK": crescimento_estimado > pl,

        # 🏛️ Heurísticas e Estratégias
        "ProxMax": preco > max52 * 0.9,
        "Acumulando?": abs(ativo["regularMarketChangePercent"]) < 0.2 and volume > 10_000_000,
        "StopLoss": preco * 0.95,
        "TakeProfit": max52 * 0.98,
        "CompraEscalonada": preco < abertura * 0.97
    }
