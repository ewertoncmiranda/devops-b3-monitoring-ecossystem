from app.dto.market_data import MarketData
"""
Combina todas as estratégias quantitativas e fundamentais para tomar decisões de compra
e venda, integrando Momentum, Valuation e Mean Reversion.

Esta classe é responsável apenas pela orquestração (SRP respeitado).
"""
class TradingEngine:


    def __init__(self, momentum, valuation, meanrev):
        self.momentum = momentum
        self.valuation = valuation
        self.meanrev = meanrev

    def should_buy(self, data: MarketData, indicators, sector_pe):
        """
        Um ativo deve ser comprado quando:
        - Está barato (valuation)
        - Está descontado (reversão à média)
        - Há tendência e volume (momentum)
        """
        return (
            self.valuation.should_buy(data, sector_pe) and
            self.meanrev.should_buy(data, indicators["z_score"]) and
            self.momentum.should_buy(data, indicators["ma20"], indicators["volume_score"])
        )

    def should_sell(self, data: MarketData, indicators, sector_pe):
        """
        Um ativo deve ser vendido quando:
        - Perdeu a tendência
        - Está caro para o setor
        - Está esticado estatisticamente
        """
        return (
            self.valuation.should_sell(data, sector_pe) or
            self.meanrev.should_sell(data, indicators["z_score"]) or
            self.momentum.should_sell(data, indicators["ma20"], indicators["volume_score"])
        )
