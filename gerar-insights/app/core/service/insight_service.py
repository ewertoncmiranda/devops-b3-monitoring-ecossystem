class InsightsService:
    """
    Gera insights qualitativos além dos sinais de compra e venda.

    Os insights abrangem:
    1. Volatilidade (risco)
    2. Força do volume (pressão institucional)
    3. Valuation justo (P/L vs setor)
    4. Momento do mercado (sentimento)
    5. Posição técnica (suporte/resistência)
    6. Saúde da tendência (tendência atual)
    """

    def gerar_insights(self, data, indicators, sector_pe):
        insights = []

        # 1️⃣ Volatilidade (risco)
        if indicators["z_score"] is not None:
            if abs(indicators["z_score"]) > 1.5:
                insights.append("Alta volatilidade — risco elevado no curto prazo.")
            else:
                insights.append("Baixa volatilidade — mercado estável.")

        # 2️⃣ Força do volume (institucional)
        vs = indicators["volume_score"]
        if vs > 1.3:
            insights.append("Volume muito acima da média — possível entrada institucional.")
        elif vs < 0.7:
            insights.append("Volume fraco — pouca força na movimentação.")
        else:
            insights.append("Volume normal — sem pressão relevante.")

        # 3️⃣ Valuation (preço justo)
        pe = data.price_earnings
        if pe < sector_pe * 0.8:
            insights.append("A ação está barata comparada ao setor — potencial de valorização.")
        elif pe > sector_pe * 1.2:
            insights.append("A ação está cara comparada ao setor — atenção ao risco.")
        else:
            insights.append("A ação está em linha com o setor — valuation neutro.")

        # 4️⃣ Momento do mercado
        if data.price >= data.fifty_two_week_high * 0.95:
            insights.append("Preço próximo da máxima anual — otimismo forte do mercado.")
        elif data.price <= data.fifty_two_week_low * 1.05:
            insights.append("Preço próximo da mínima anual — possível oportunidade de reversão.")
        else:
            insights.append("Preço em zona neutra — sem emoções extremas no mercado.")

        # 5️⃣ Posição técnica (suporte/resistência)
        if data.price <= data.fifty_two_week_low * 1.02:
            insights.append("Ativo está batendo no suporte anual.")
        if data.price >= data.fifty_two_week_high * 0.98:
            insights.append("Ativo está encontrando resistência próxima do topo anual.")

        # 6️⃣ Saúde da tendência (tendência forte, fraca ou neutra)
        ma20 = indicators["ma20"]
        if ma20:
            if data.price > ma20 * 1.02:
                insights.append("Tendência forte de alta no curto prazo.")
            elif data.price < ma20 * 0.98:
                insights.append("Tendência de queda no curto prazo.")
            else:
                insights.append("Tendência neutra — sem direção definida.")

        return insights
