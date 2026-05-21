import json
import time
from dataclasses import dataclass
from logging import Logger

from app.config.aws_config import AwsConfig
from app.config.database_config import ConfigDatabase
from app.core.mapper.equity_snapshot import SnapshotAcao
from app.core.service.financial_analyzer_service import FinancialAnalyzerService
from app.core.service.persistencia_service import PersistenciaHistoricoService
from app.external.database.entity.insight_entity import InsightEntity
from app.external.database.insight_repository import InsightRepository


@dataclass
class CoreProcessor:
    logger: Logger
    historico_service: PersistenciaHistoricoService
    financial_analyzer: FinancialAnalyzerService
    insight_repository: InsightRepository
    aws: AwsConfig
    session_db: None

    @staticmethod
    def instanciar(logger: Logger):
        persistence = PersistenciaHistoricoService()
        financial_analyzer = FinancialAnalyzerService(logger=logger)
        session_db = ConfigDatabase().session
        insight_repository = InsightRepository(db=session_db, logger=logger)
        aws = AwsConfig()
        return CoreProcessor(logger=logger,
                             historico_service=persistence,
                             financial_analyzer=financial_analyzer,
                             insight_repository=insight_repository,
                             aws=aws,
                             session_db=session_db)

    def consume_messages(self, queue_url: str):
        while True:
            try:
                resp = self.aws.get_sqs_client().receive_message(
                    QueueUrl=queue_url,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=10
                )
                messages = resp.get('Messages', [])

                if not messages:
                    self.logger.info("Nenhuma mensagem na fila; aguardando...")
                    continue

                for m in messages:
                    receipt_handle = m['ReceiptHandle']
                    try:
                        ativo = json.loads(m['Body'])
                        self.processar_persistencia(ativo)
                        insight_dict = self.financial_analyzer.gerar_insight_fundamentalista(ativo)
                        self.salvar_insight(insight_dict)
                        self.aws.get_sqs_client().delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                        self.logger.info("Mensagem processada e deletada com sucesso")

                    except (json.JSONDecodeError, ValueError, TypeError) as bad_data_err:

                        self.logger.error(f"Payload inválido. Descartando mensagem: {bad_data_err}")
                        self.aws.get_sqs_client().delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                    except Exception as process_err:
                        self.logger.error(f"Erro ao processar ativo. Mantendo na fila para retry: {process_err}",
                                          exc_info=True)

            except Exception as loop_err:
                self.logger.error(f"Erro crítico no loop SQS: {loop_err}")
                time.sleep(5)

    def processar_persistencia(self, ativo):
        snapshot = SnapshotAcao(ativo)
        self.logger.info(f"Iniciando persistencia do objeto: {snapshot}")
        try:
            self.historico_service.registrar_snapshot(self.session_db, snapshot)
        finally:
            self.session_db.close()

    def salvar_insight(self, insight_dict):

        try:
            entidade = InsightEntity(
                simbolo=insight_dict["simbolo"],
                preco_justo_graham=insight_dict["preco_justo_graham"],
                margem_seguranca_percent=insight_dict["margem_seguranca_percent"],
                recomendacao=insight_dict["recomendacao"],
                detalhes_json=insight_dict["detalhes_json"]
            )
            self.insight_repository.salvar(self.session_db, entidade)
        finally:
            self.session_db.close()
