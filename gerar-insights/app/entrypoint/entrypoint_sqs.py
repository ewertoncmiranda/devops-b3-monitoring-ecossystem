import json
import time

from botocore.exceptions import ClientError, ReadTimeoutError

from app.config.aws_config import sqs
from app.config.config_logger import setup_logger
from app.config.database_config import SessionLocal
from app.core.mapper.equity_snapshot import SnapshotAcao
from app.core.service.persistencia_service import PersistenciaHistoricoService
from app.core.service.trading_service import TradingService
from app.core.view.charts import gerar_todos_os_graficos

logger = setup_logger()
persistencia_service = PersistenciaHistoricoService()


def ensure_queue(name: str) -> str:
    try:
        logger.info("validando fila sqs :")
        return sqs.get_queue_url(QueueName=name)['QueueUrl']
    except ClientError as e:
        logger.info("FILA NÃO EXISTENTE")
        raise e


def consume_messages(queue_url: str):
    while True:
        try:
            resp = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10
            )
            messages = resp.get('Messages', [])

            if not messages:
                logger.info("Nenhuma mensagem; aguardando...")

            for m in messages:
                logger.info(f"Recebido: {m['Body']}")
                try:
                    mesg = m['Body']
                    ativo = json.loads(mesg)
                    logger.info(f" Processando mensagem : {mesg}")

                    insight_single(ativo)
                    snapshot = SnapshotAcao(ativo)

                    logger.info(f" Iniciando persistencia do objeto: : {snapshot}")
                    db = SessionLocal()
                    persistencia_service.registrar_snapshot(db, snapshot)

                    processar_ativo = TradingService()
                    decisao, indicadores, insights = processar_ativo.processar_ativo(ativo)

                    gerar_todos_os_graficos(ativo,indicadores)
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=m['ReceiptHandle']
                    )

                except Exception as process_err:
                    logger.error(
                        f"Erro ao processar mensagem específica: {process_err}",
                        exc_info=True
                    )

        except ReadTimeoutError:
            logger.warning("ReadTimeout: sem resposta, tentando novamente...")
        except ClientError as e:
            logger.error(f"AWS ClientError: {e}", exc_info=True)
        except Exception as e:
            logger.error("Erro ao consumir mensagens", exc_info=True)

        time.sleep(30)


def insight_single(ativo):
    trading = TradingService()
    decisao, indicadores, insights = trading.processar_ativo(ativo)
    logger.info(f"🟢 Decisão: {decisao}")
    logger.info(f"🔣 Indicadores: {indicadores}")
    logger.info(f"💡 Insights: {insights}")
