# app/services/trading_service.py

from app.dto.market_data import MarketData
from app.core.service.indicator_service import IndicatorsService
from app.core.service.insight_service import InsightsService

from app.core.trading_engine import TradingEngine
from app.core.strategies.momentum_strategy import MomentumStrategy
from app.core.strategies.valuation_strategy import ValuationStrategy
from app.core.strategies.mean_reversion_strategy import MeanReversionStrategy


class TradingService:
    """
    Serviço responsável por integrar:
    - MarketData (entrada bruta)
    - IndicatorsService (cálculo técnico e estatístico)
    - TradingEngine (lógica de compra e venda)
    - InsightsService (gera insights adicionais)
    """

    def __init__(self):
        self.indicators_service = IndicatorsService()
        self.insights_service = InsightsService()

        self.engine = TradingEngine(
            MomentumStrategy(),
            ValuationStrategy(),
            MeanReversionStrategy()
        )

    def processar_ativo(self, payload_dict: dict):
        """
        Recebe o JSON vindo da fila, converte para MarketData,
        calcula indicadores, executa estratégias quantitativas
        e gera insights adicionais.
        """

        # 1 — Converte o payload para MarketData
        data = MarketData(payload_dict)

        # 2 — Em produção: recuperar histórico real do SQL
        # Aqui mockamos para demonstrar o fluxo completo.
        historical_prices = [
            data.price * 0.98,
            data.price * 0.97,
            data.price * 1.02,
            data.price * 1.01,
            data.price
        ]

        historical_volumes = [
            data.day_volume * 0.8,
            data.day_volume * 0.9,
            data.day_volume * 1.1,
            data.day_volume * 0.7,
            data.day_volume
        ]

        # 3 — Cálculo dos indicadores via serviço dedicado
        indicators = self.indicators_service.calcular_indicadores(
            data,
            historical_prices,
            historical_volumes
        )

        # 4 — Em produção: puxar do banco P/L médio do setor
        sector_pe = 10

        # 5 — Decisão de compra/venda
        if self.engine.should_buy(data, indicators, sector_pe):
            decisao = "COMPRAR"
        elif self.engine.should_sell(data, indicators, sector_pe):
            decisao = "VENDER"
        else:
            decisao = "MANTER"

        # 6 — Insights adicionais (6 insights novos)
        insights = self.insights_service.gerar_insights(
            data,
            indicators,
            sector_pe
        )

        return decisao, indicators, insights
