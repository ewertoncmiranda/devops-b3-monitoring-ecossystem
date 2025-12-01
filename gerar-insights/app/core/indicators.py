# indicators.py
import numpy as np


class IndicatorsCalculator:
    """
    Calcula indicadores estatísticos e técnicos essenciais para as estratégias quantitativas:
    - Médias móveis para detecção de tendência (Momentum Strategy)
    - Volatilidade histórica para stops e gestão de risco
    - Volume médio para detectar entrada ou saída institucional
    - Z-Score para reversão à média (Mean Reversion Strategy)
    """

    @staticmethod
    def moving_average(series, window):
        """
        Calcula média móvel simples (SMA).

        Usado para:
        - Identificar tendência (Momentum Strategy)
        - Definir níveis de suporte/resistência
        """
        if len(series) < window:
            return None
        return np.mean(series[-window:])

    @staticmethod
    def volatility(series, window):
        """
        Calcula volatilidade (desvio padrão).

        Usado para:
        - Stops inteligentes
        - Gestão de risco
        """
        if len(series) < window:
            return None
        return float(np.std(series[-window:]))

    @staticmethod
    def volume_score(current_volume, historical_volumes):
        """
        Compara o volume atual com a média histórica dos últimos 20 dias/minutos.

        Volume alto indica:
        - Pressão compradora/vendedora
        - Entrada ou saída institucional
        """
        avg = np.mean(historical_volumes[-20:])
        return current_volume / avg

    @staticmethod
    def z_score(series, window):
        """
        Calcula Z-Score do preço.

        Serve como núcleo da estratégia de Reversão à Média (Mean Reversion):
        - z < -2 → compra (preço muito descontado)
        - z > +2 → venda (preço esticado)
        """
        if len(series) < window:
            return None

        mean = np.mean(series[-window:])
        std = np.std(series[-window:])
        return (series[-1] - mean) / std if std > 0 else 0
