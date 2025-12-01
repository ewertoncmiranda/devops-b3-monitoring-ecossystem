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

    logo_url TEXT
);



INSERT INTO ativos (
    symbol, currency, short_name, long_name,
    market_cap, market_change, market_change_percent,
    regular_market_time, regular_market_price,
    regular_market_day_high, regular_market_day_low,
    regular_market_day_range, regular_market_volume,
    regular_market_previous_close, regular_market_open,
    fifty_two_week_range, fifty_two_week_low, fifty_two_week_high,
    price_earnings, earnings_per_share, logo_url
) VALUES
-- PETR4
(
    'PETR4', 'BRL', 'Petrobras PN', 'Petróleo Brasileiro S.A. - Petrobras',
    530000000000.00, 1.85, 1.12,
    '2025-01-15 16:00:00', 33.50,
    34.10, 33.00,
    '33.00 - 34.10', 18900000.00,
    32.98, 33.10,
    '20.50 - 37.40', 20.50, 37.40,
    3.80, 8.79, 'https://logo.clearbit.com/petrobras.com.br'
),

-- VALE3
(
    'VALE3', 'BRL', 'Vale ON', 'Vale S.A.',
    310000000000.00, -0.90, -0.55,
    '2025-01-15 16:00:00', 68.30,
    69.10, 67.50,
    '67.50 - 69.10', 12300000.00,
    68.80, 68.90,
    '61.00 - 82.10', 61.00, 82.10,
    5.40, 12.65, 'https://logo.clearbit.com/vale.com'
),

-- ITUB4
(
    'ITUB4', 'BRL', 'Itaú Unibanco PN', 'Itaú Unibanco Holding S.A.',
    290000000000.00, 0.35, 0.42,
    '2025-01-15 16:00:00', 26.50,
    26.80, 26.20,
    '26.20 - 26.80', 16000000.00,
    26.39, 26.45,
    '22.30 - 29.70', 22.30, 29.70,
    8.20, 3.22, 'https://logo.clearbit.com/itau.com.br'
),

-- ABEV3
(
    'ABEV3', 'BRL', 'Ambev ON', 'Ambev S.A.',
    240000000000.00, -0.12, -0.28,
    '2025-01-15 16:00:00', 14.60,
    14.80, 14.40,
    '14.40 - 14.80', 42000000.00,
    14.64, 14.70,
    '12.00 - 17.90', 12.00, 17.90,
    21.50, 0.68, 'https://logo.clearbit.com/ambev.com.br'
);
