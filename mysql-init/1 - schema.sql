CREATE TABLE IF NOT EXISTS ativos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    symbol VARCHAR(50),
    currency VARCHAR(20),

    short_name VARCHAR(255),
    long_name VARCHAR(255),

    market_cap DECIMAL(20,2),
    market_change DECIMAL(20,2),
    market_change_percent DECIMAL(20,2),

    regular_market_time DATETIME,

    regular_market_price DECIMAL(20,2),
    regular_market_day_high DECIMAL(20,2),
    regular_market_day_low DECIMAL(20,2),

    regular_market_day_range VARCHAR(100),

    regular_market_volume DECIMAL(20,2),
    regular_market_previous_close DECIMAL(20,2),
    regular_market_open DECIMAL(20,2),

    fifty_two_week_range VARCHAR(100),
    fifty_two_week_low DECIMAL(20,2),
    fifty_two_week_high DECIMAL(20,2),

    price_earnings DECIMAL(20,2),
    earnings_per_share DECIMAL(20,2),

    logo_url TEXT,

    -- Índices para melhor performance
    INDEX idx_symbol (symbol),
    INDEX idx_regular_market_time (regular_market_time)
);

-- Tabela de histórico de ativos
CREATE TABLE IF NOT EXISTS historico_acoes (
    id INT AUTO_INCREMENT PRIMARY KEY,

    simbolo VARCHAR(10) NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    preco_abertura DECIMAL(12,4),
    preco_fechamento DECIMAL(12,4),
    preco_maximo DECIMAL(12,4),
    preco_minimo DECIMAL(12,4),

    volume BIGINT,

    minima_52_semanas DECIMAL(12,4),
    maxima_52_semanas DECIMAL(12,4),

    valor_mercado BIGINT,
    preco_lucro DECIMAL(10,4),
    lucro_por_acao DECIMAL(10,4),

    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Índices para melhor performance
    INDEX idx_simbolo (simbolo),
    INDEX idx_timestamp (timestamp),
    INDEX idx_simbolo_timestamp (simbolo, timestamp)
);
