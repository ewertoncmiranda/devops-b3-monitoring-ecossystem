class TradingService:
    """
    Serviço responsável por processar o ativo recebido,
    calcular indicadores e decidir uma ação (Comprar/Vender/Manter).
    """

    def processar_ativo(self, ativo: dict):
        indicadores = self.calcular_indicadores(ativo)
        decisao = self.calcular_decisao(indicadores)
        insights = self.gerar_insights(indicadores)
        return decisao, indicadores, insights

    def calcular_indicadores(self, ativo: dict) -> dict:
        preco = ativo.get("regularMarketPrice")
        abertura = ativo.get("regularMarketOpen")
        max_dia = ativo.get("regularMarketDayHigh")
        min_dia = ativo.get("regularMarketDayLow")
        volume = ativo.get("regularMarketVolume")
        pl = ativo.get("priceEarnings")
        lpa = ativo.get("earningsPerShare")
        max52 = ativo.get("fiftyTwoWeekHigh")
        min52 = ativo.get("fiftyTwoWeekLow")
        market_cap = ativo.get("marketCap")

        indicadores = {
            # --- Indicadores técnicos básicos ---
            "oscilacao_dia_percentual": (
                ((max_dia - min_dia) / abertura) * 100
                if abertura else None
            ),
            "variacao_abertura": (
                ((preco - abertura) / abertura) * 100
                if abertura else None
            ),

            # --- Indicadores fundamentalistas ---
            "pl": pl,
            "lpa": lpa,
            "earnings_yield": (
                (lpa / preco) * 100
                if preco else None
            ),
            "valor_mercado": market_cap,

            # --- Indicadores de risco / volatilidade ---
            "range_52_semanas": (
                max52 - min52
                if max52 and min52 else None
            ),
            "posicao_no_range_52w_percent": (
                (preco - min52) / (max52 - min52) * 100
                if preco and max52 and min52 and max52 != min52 else None
            ),

            # --- Volume ---
            "volume_hoje": volume,
        }

        return indicadores

    # ---------------------------------------------------------------------

    def calcular_decisao(self, indicadores: dict) -> str:
        """
        Regras simplificadas de compra/venda baseadas nos indicadores.
        """

        if indicadores["earnings_yield"] and indicadores["earnings_yield"] > 12:
            return "COMPRAR"

        if indicadores["variacao_abertura"] and indicadores["variacao_abertura"] < -3:
            return "VENDER"

        return "MANTER"

    # ---------------------------------------------------------------------

    def gerar_insights(self, indicadores: dict) -> list:
        insights = []

        if indicadores["earnings_yield"] and indicadores["earnings_yield"] > 12:
            insights.append("A ação está barata em termos de retorno sobre lucro.")

        if indicadores["posicao_no_range_52w_percent"] is not None:
            if indicadores["posicao_no_range_52w_percent"] > 80:
                insights.append("Preço perto da máxima de 52 semanas.")

            if indicadores["posicao_no_range_52w_percent"] < 20:
                insights.append("Preço próximo da mínima anual.")

        if indicadores["oscilacao_dia_percentual"] and indicadores["oscilacao_dia_percentual"] < 1:
            insights.append("Baixa volatilidade no dia.")

        if not insights:
            insights.append("Nenhum sinal forte encontrado.")

        return insights

    # ---------------------------------------------------------------------


