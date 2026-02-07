# app/core/service/insight_orchestrator.py
import time
import json

from app.config.enhanced_json import EnhancedJSONEncoder
from app.external.database.insights_repository import DatabaseService
from app.core.service.aggregator_service import AggregatorService
from app.core.service.trading_service import TradingService

class ProcessamentoMetricasOrchestrator:

    def __init__(self):
        self.db = DatabaseService()
        self.aggregator = AggregatorService()
        self.trading = TradingService()

    def run(self):

        print("\n🔄 Rodando scan de ativos...")

        symbols = self.db.get_all_symbols()
        resultado_final = []

        for symbol in symbols:
            snapshot = self.db.get_latest_snapshot(symbol)
            historico = self.db.get_last_n_registros_ativos(symbol, 30)

            contexto = self.aggregator.aggregate(symbol, snapshot, historico)

            decisao, indicadores, insights = self.trading.processar_ativo(
                contexto["snapshot"]
            )

            resultado_final.append({
                "symbol": symbol,
                "contexto": contexto,
                "indicadores": indicadores,
                "decisao": decisao,
                "insights": insights
            })

        # saída rica e completa
        json_saida = json.dumps(resultado_final, indent=4, ensure_ascii=False,cls=EnhancedJSONEncoder)
        print(json_saida)

        print("\n⏳ Aguardando 2 minutos para próxima análise...\n")
        time.sleep(120)
