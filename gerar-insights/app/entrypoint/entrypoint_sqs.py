import json
import time
from botocore.exceptions import ClientError

from app.config.aws_config import sqs
from app.config.config_logger import setup_logger
from app.config.database_config import SessionLocal
from app.core.mapper.equity_snapshot import SnapshotAcao
from app.core.service.persistencia_service import PersistenciaHistoricoService
from app.core.service.financial_analyzer_service import FinancialAnalyzerService
from app.external.database.insight_repository import InsightRepository
from app.external.database.entity.insight_entity import InsightEntity

logger = setup_logger()
persistencia_service = PersistenciaHistoricoService()
financial_analyzer = FinancialAnalyzerService()
insight_repository = InsightRepository()
db = SessionLocal()

def ensure_queue(name: str) -> str:
    try:
        logger.info("validando fila sqs :")
        return sqs.get_queue_url(QueueName=name)['QueueUrl']
    except ClientError as e:
        logger.info("FILA NÃO EXISTENTE")
        raise e


def consume_messages(queue_url: str):
    """
    Consome mensagens da fila SQS em loop infinito aplicando melhores práticas.
    """
    while True:
        try:
            resp = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10
            )
            messages = resp.get('Messages', [])

            if not messages:
                logger.info("Nenhuma mensagem na fila; aguardando...")
                continue

            for m in messages:
                receipt_handle = m['ReceiptHandle']
                try:
                    ativo = json.loads(m['Body'])
                    logger.info(f"📊 Processando ativo: {ativo.get('symbol', 'UNKNOWN')}")

                    # 1. Persiste histórico bruto
                    processar_persistencia(ativo)

                    # 2. Processa insights financeiros objetivos
                    insight_dict = financial_analyzer.gerar_insight_fundamentalista(ativo)
                    
                    # 3. Salva insight no banco
                    salvar_insight(insight_dict)

                    # 4. Deleta com sucesso
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                    logger.info("✅ Mensagem processada e deletada com sucesso")

                except (json.JSONDecodeError, ValueError, TypeError) as bad_data_err:
                    # Erro de formatação (payload zoadom). Delete para não travar a fila em loop
                    logger.error(f"❌ Payload inválido. Descartando mensagem: {bad_data_err}")
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                except Exception as process_err:
                    # Erro de infraestrutura (banco fora, etc). NÃO deletar, permite retry na fila.
                    logger.error(f"❌ Erro ao processar ativo. Mantendo na fila para retry: {process_err}", exc_info=True)

        except Exception as loop_err:
            logger.error(f"❌ Erro crítico no loop SQS: {loop_err}")
            time.sleep(5)  # Backoff de segurança para não explodir CPU em caso de queda de rede


def processar_persistencia(ativo):
    snapshot = SnapshotAcao(ativo)
    logger.info(f"Iniciando persistencia do objeto: {snapshot}")
    try:
        persistencia_service.registrar_snapshot(db, snapshot)
    finally:
        db.close()

def salvar_insight(insight_dict):

    try:
        entidade = InsightEntity(
            simbolo=insight_dict["simbolo"],
            preco_justo_graham=insight_dict["preco_justo_graham"],
            margem_seguranca_percent=insight_dict["margem_seguranca_percent"],
            recomendacao=insight_dict["recomendacao"],
            detalhes_json=insight_dict["detalhes_json"]
        )
        insight_repository.salvar(db, entidade)
    finally:
        db.close()
