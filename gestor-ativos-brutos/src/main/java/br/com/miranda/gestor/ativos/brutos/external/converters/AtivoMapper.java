/*
package br.com.miranda.gestor.ativos.brutos.mapper;

import br.com.miranda.gestor.ativos.brutos.entidade.Ativo;
import br.com.miranda.gestor.ativos.brutos.external.dto.BrapiAtivoDTO;
import org.mapstruct.*;
import org.mapstruct.factory.Mappers;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Mapper(componentModel = "spring", imports = {BigDecimal.class, LocalDateTime.class})
public interface AtivoMapper {

    AtivoMapper INSTANCE = Mappers.getMapper(AtivoMapper.class);

    @Mappings({
            @Mapping(target = "id", ignore = true),
            @Mapping(target = "marketCap", expression = "java(toBigDecimal(dto.getMarketCap()))"),
            @Mapping(target = "regularMarketChange", expression = "java(toBigDecimal(dto.getRegularMarketChange()))"),
            @Mapping(target = "regularMarketChangePercent", expression = "java(toBigDecimal(dto.getRegularMarketChangePercent()))"),
            @Mapping(target = "regularMarketTime", expression = "java(toDateTime(dto.getRegularMarketTime()))"),
            @Mapping(target = "regularMarketPrice", expression = "java(toBigDecimal(dto.getRegularMarketPrice()))"),
            @Mapping(target = "regularMarketDayHigh", expression = "java(toBigDecimal(dto.getRegularMarketDayHigh()))"),
            @Mapping(target = "regularMarketDayLow", expression = "java(toBigDecimal(dto.getRegularMarketDayLow()))"),
            @Mapping(target = "regularMarketVolume", expression = "java(toBigDecimal(String.valueOf(dto.getRegularMarketVolume())))"),
            @Mapping(target = "regularMarketPreviousClose", expression = "java(toBigDecimal(dto.getRegularMarketPreviousClose()))"),
            @Mapping(target = "regularMarketOpen", expression = "java(toBigDecimal(dto.getRegularMarketOpen()))"),
            @Mapping(target = "fiftyTwoWeekLow", expression = "java(toBigDecimal(dto.getFiftyTwoWeekLow()))"),
            @Mapping(target = "fiftyTwoWeekHigh", expression = "java(toBigDecimal(dto.getFiftyTwoWeekHigh()))"),
            @Mapping(target = "priceEarnings", expression = "java(toBigDecimal(dto.getPriceEarnings()))"),
            @Mapping(target = "earningsPerShare", expression = "java(toBigDecimal(dto.getEarningsPerShare()))")
    })
    Ativo toEntity(BrapiAtivoDTO dto);

    // Métodos auxiliares para conversão

    default BigDecimal toBigDecimal(String value) {
        try {
            return value != null && !value.isBlank() ? new BigDecimal(value) : null;
        } catch (NumberFormatException e) {
            return null;
        }
    }

    default LocalDateTime toDateTime(String isoDateTime) {
        try {
            return isoDateTime != null ? LocalDateTime.parse(isoDateTime, DateTimeFormatter.ISO_DATE_TIME) : null;
        } catch (Exception e) {
            return null;
        }
    }
}
*/
