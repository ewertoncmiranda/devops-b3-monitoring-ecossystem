import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "/app/output_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def chart_price_range(ativo):
    """Gráfico da faixa de preço diária."""
    preco = ativo["regularMarketPrice"]
    high = ativo["regularMarketDayHigh"]
    low = ativo["regularMarketDayLow"]

    fig, ax = plt.subplots()
    ax.plot(["Low", "Price", "High"], [low, preco, high])
    ax.set_title(f"{ativo['symbol']} - Daily Price Range")

    filename = f"{OUTPUT_DIR}/{ativo['symbol']}_price_range.png"
    plt.savefig(filename)
    plt.close()
    return filename


def chart_52w_range(ativo):
    """Faixa de preço das 52 semanas."""
    preco = ativo["regularMarketPrice"]
    low52 = ativo["fiftyTwoWeekLow"]
    high52 = ativo["fiftyTwoWeekHigh"]

    fig, ax = plt.subplots()
    ax.plot(["52w Low", "Current", "52w High"], [low52, preco, high52])
    ax.set_title(f"{ativo['symbol']} - 52 Week Range")

    filename = f"{OUTPUT_DIR}/{ativo['symbol']}_52w_range.png"
    plt.savefig(filename)
    plt.close()
    return filename


def chart_indicators(indicators, symbol):
    """Indicadores técnicos e quantitativos normalizados."""
    keys = list(indicators.keys())
    values = [float(indicators[k]) for k in keys]

    fig, ax = plt.subplots()
    ax.bar(keys, values)
    plt.xticks(rotation=45, ha="right")
    ax.set_title(f"{symbol} - Indicators")

    filename = f"{OUTPUT_DIR}/{symbol}_indicators.png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()
    return filename


def chart_volume_marketcap(ativo):
    """Volume e MarketCap escalados."""
    volume = ativo["regularMarketVolume"]
    market_cap = ativo["marketCap"]

    fig, ax = plt.subplots()
    ax.bar(["Volume", "MarketCap"], [volume, market_cap])
    ax.set_title(f"{ativo['symbol']} - Volume vs MarketCap")

    filename = f"{OUTPUT_DIR}/{ativo['symbol']}_volume_mc.png"
    plt.savefig(filename)
    plt.close()
    return filename


def gerar_todos_os_graficos(ativo, indicadores):
    """Função única que gera tudo e retorna os arquivos."""
    files = {}
    files["price_range"] = chart_price_range(ativo)
    files["52w_range"] = chart_52w_range(ativo)
    files["indicators"] = chart_indicators(indicadores, ativo["symbol"])
    files["volume_marketcap"] = chart_volume_marketcap(ativo)
    return files
