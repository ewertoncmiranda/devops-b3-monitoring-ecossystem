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
