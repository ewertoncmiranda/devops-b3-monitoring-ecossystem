from app.core.indicators import IndicatorsCalculator
"""
Serviço responsável por calcular indicadores técnicos e estatísticos.
Esta classe funciona como uma camada intermediária entre os dados brutos
e os cálculos disponibilizados por IndicatorsCalculator.

Agora suporta:
- Execução com pouco histórico (modo teste local)
- Ajuste automático da janela (auto-window)
- Garantia de que nenhum indicador retornará valores inválidos
"""

class IndicatorsService:

    def _calcular_janela(self, historical_prices, max_window=20):
        """
        Determina automaticamente a janela de cálculo com base no histórico disponível.

        - Se houver 20 ou mais elementos, usa 20.
        - Caso contrário, usa o máximo possível (>= 2).
        - Se houver apenas 1 elemento, retorna None (indicador não calculável).
        """
        tamanho = len(historical_prices)

        if tamanho >= max_window:
            return max_window

        if tamanho >= 2:
            return tamanho

        return None

    def calcular_indicadores(self, data, historical_prices, historical_volumes):
        """
        Calcula indicadores essenciais:
        - MA20 (ou MA variável para testes)
        - Z-Score (estatístico)
        - Volume Score

        Todos com fallback seguro para testes locais.
        """

        # 1. Determinar janela de cálculo
        window = self._calcular_janela(historical_prices)

        # === Trata indicadores indisponíveis ===
        if window is None:
            return {
                "ma20": None,
                "z_score": None,
                "volume_score": 1  # volume neutro
            }

        # 2. Cálculo da média móvel (MA)
        ma20 = IndicatorsCalculator.moving_average(
            series=historical_prices,
            window=window
        )

        # 3. Cálculo do z-score estatístico
        z_score = IndicatorsCalculator.z_score(
            series=historical_prices,
            window=window
        )

        # 4. Volume Score sempre pode ser calculado
        volume_score = IndicatorsCalculator.volume_score(
            current_volume=data.day_volume,
            historical_volumes=historical_volumes
        )

        return {
            "ma20": ma20,
            "z_score": z_score,
            "volume_score": volume_score
        }
