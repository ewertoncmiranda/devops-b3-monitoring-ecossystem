# Quantitative Trading Strategies – Python SRP Architecture

Este projeto implementa uma arquitetura completa de trading algorítmico baseada em:

- Momentum Strategy  
- Valuation Strategy  
- Mean Reversion Strategy  
- Indicadores estatísticos (MA, Volatilidade, Volume, Z-Score)
- Orquestrador de estratégias (Trading Engine)

Todo o código segue **SRP (Single Responsibility Principle)**, totalmente modular e pronto para produção.

---

# 📌 Estratégias Implementadas

## 1. Momentum Strategy
Usa:
- Média móvel de 20 períodos
- Volume acima da média

Compra quando:
- Preço cruza para cima da média móvel  
- Volume > média × 1.3

Venda quando:
- Preço cruza para baixo  
- Volume baixo indica fim da tendência

---

## 2. Valuation Strategy (Fundamentalista)
Compra quando:
- P/L da empresa < P/L do setor × 0.80

Venda quando:
- P/L > P/L do setor × 1.10

---

## 3. Mean Reversion Strategy
Compra quando:
- Z-Score < -1.5  
- Preço perto do 52-week low

Venda quando:
- Z-Score > +1.5  
- Preço perto do 52-week high

---

# 📌 Indicadores Calculados
- SMA (MA5, MA20, MA50)
- Volatilidade histórica (std)
- Volume score (volume atual / média dos últimos 20)
- Z-Score (desvio do preço em relação à média)

---

# 📌 Trading Engine
A classe **TradingEngine** combina:

- Momentum  
- Valuation  
- Mean Reversion  

E toma a decisão final de compra ou venda.

Regra para compra:
```
cheap AND discounted AND rising_with_volume
```

Regra para venda:
```
expensive OR overbought OR losing_momentum
```

---

# 📌 Estrutura de Pastas

```
/project
  /strategies
    momentum_strategy.py
    valuation_strategy.py
    mean_reversion_strategy.py
  /core
    market_data.py
    indicators.py
    trading_engine.py
  README.md
```

---

# 📌 Como Usar

```python
data = MarketData(payload)

indicators = {
    "ma20": IndicatorsCalculator.moving_average(price_series, 20),
    "z_score": IndicatorsCalculator.z_score(price_series, 50),
    "volume_score": IndicatorsCalculator.volume_score(data.day_volume, volume_series)
}

engine = TradingEngine(
    MomentumStrategy(),
    ValuationStrategy(),
    MeanReversionStrategy()
)

if engine.should_buy(data, indicators, sector_pe=12):
    print("Comprar")
elif engine.should_sell(data, indicators, sector_pe=12):
    print("Vender")
```

---

# 📌 Objetivo

Criar um sistema algorítmico completo capaz de:
- avaliar dados da B3
- gerar sinais de compra e venda
- combinar análise fundamentalista e quantitativa
- servir de base para arbitragem, swing trade, long & short e position

---

# 📌 Licença
MIT
