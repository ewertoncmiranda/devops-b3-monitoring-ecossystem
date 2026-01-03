import numpy as np

class AggregatorService:

    @staticmethod
    def aggregate(symbol: str, snapshot, historico: list):
        prices = [h.preco_fechamento for h in historico if h.preco_fechamento]
        volumes = [h.volume for h in historico if h.volume]

        return {
            "symbol": symbol,
            "snapshot": {
                "preco": snapshot.regular_market_price,
                "abertura": snapshot.regular_market_open,
                "max_dia": snapshot.regular_market_day_high,
                "min_dia": snapshot.regular_market_day_low,
                "volume": snapshot.regular_market_volume,
                "pl": snapshot.price_earnings,
                "lpa": snapshot.earnings_per_share,
                "marketcap": snapshot.market_cap,
                "min_52": snapshot.fifty_two_week_low,
                "max_52": snapshot.fifty_two_week_high
            },
            "historico": {
                "ultimos_precos": prices,
                "ultimos_volumes": volumes,
                "media_20": float(np.mean(prices[-20:])) if len(prices) >= 20 else None,
                "max_30dias": max(prices) if prices else None,
                "min_30dias": min(prices) if prices else None,
                "vol_medio_30d": float(np.mean(volumes)) if volumes else None,
            }
        }
