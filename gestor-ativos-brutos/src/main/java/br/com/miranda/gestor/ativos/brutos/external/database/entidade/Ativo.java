package br.com.miranda.gestor.ativos.brutos.external.database.entidade;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "ativos")
@Data
@AllArgsConstructor
@Getter
@NoArgsConstructor
public class Ativo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "symbol")
    private String symbol;

    @Column(name = "currency")
    private String currency;

    @Column(name = "short_name")
    private String shortName;

    @Column(name = "long_name")
    private String longName;

    @Column(name = "market_cap", precision = 20, scale = 2)
    private BigDecimal marketCap;

    @Column(name = "market_change", precision = 20, scale = 2)
    private BigDecimal regularMarketChange;

    @Column(name = "market_change_percent", precision = 20, scale = 2)
    private BigDecimal regularMarketChangePercent;

    @Column(name = "regular_market_time")
    private LocalDateTime regularMarketTime;

    @Column(name = "regular_market_price", precision = 20, scale = 2)
    private BigDecimal regularMarketPrice;

    @Column(name = "regular_market_day_high", precision = 20, scale = 2)
    private BigDecimal regularMarketDayHigh;

    @Column(name = "regular_market_day_low", precision = 20, scale = 2)
    private BigDecimal regularMarketDayLow;

    @Column(name = "regular_market_day_range")
    private String regularMarketDayRange;

    @Column(name = "regular_market_volume", precision = 20, scale = 2)
    private BigDecimal regularMarketVolume;

    @Column(name = "regular_market_previous_close", precision = 20, scale = 2)
    private BigDecimal regularMarketPreviousClose;

    @Column(name = "regular_market_open", precision = 20, scale = 2)
    private BigDecimal regularMarketOpen;

    @Column(name = "fifty_two_week_range")
    private String fiftyTwoWeekRange;

    @Column(name = "fifty_two_week_low", precision = 20, scale = 2)
    private BigDecimal fiftyTwoWeekLow;

    @Column(name = "fifty_two_week_high", precision = 20, scale = 2)
    private BigDecimal fiftyTwoWeekHigh;

    @Column(name = "price_earnings", precision = 20, scale = 2)
    private BigDecimal priceEarnings;

    @Column(name = "earnings_per_share", precision = 20, scale = 2)
    private BigDecimal earningsPerShare;

    @Column(name = "logo_url")
    private String logoUrl;
}
