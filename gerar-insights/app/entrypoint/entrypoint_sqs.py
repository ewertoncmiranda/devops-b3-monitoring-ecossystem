import json
import time

from botocore.exceptions import ClientError, ReadTimeoutError

from app.config.aws_config import sqs
from app.config.config_logger import setup_logger
from app.config.database_config import SessionLocal
from app.core.mapper.equity_snapshot import SnapshotAcao
from app.core.service.persistencia_service import PersistenciaHistoricoService
from app.core.service.trading_service import TradingService
from app.entrypoint.processamento_metricas import ProcessamentoMetricasOrchestrator
from app.exceptions import QueueProcessingError, InvalidAtivoError, DatabaseError, TradingAnalysisError

logger = setup_logger()
persistencia_service = PersistenciaHistoricoService()
processar_metricas = ProcessamentoMetricasOrchestrator()


def ensure_queue(name: str) -> str:
    try:
        logger.info("validando fila sqs :")
        return sqs.get_queue_url(QueueName=name)['QueueUrl']
    except ClientError as e:
        logger.info("FILA NÃO EXISTENTE")
        raise e


def consume_messages(queue_url: str):
    """
    Consome mensagens da fila SQS em loop infinito.
    Processa cada mensagem: análise de trading, persistência e orquestração.
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
                logger.info("Nenhuma mensagem na fila; aguardando próxima verificação...")

            for m in messages:
                receipt_handle = m['ReceiptHandle']
                try:
                    mesg = m['Body']
                    logger.info(f"✓ Mensagem recebida: {mesg}")

                    ativo = json.loads(mesg)
                    logger.info(f"📊 Processando ativo: {ativo.get('symbol', 'UNKNOWN')}")

                    # Processa insights
                    processar_info(ativo)

                    # Persiste histórico
                    processar_persistencia(ativo)

                    # Orquestra métricas gerais
                    processar_metricas.run()

                    # Delete com sucesso
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    logger.info(f"✅ Mensagem processada e deletada com sucesso")

                except json.JSONDecodeError as je:
                    logger.error(f"❌ Erro ao fazer parse JSON da mensagem: {je}", exc_info=True)
                    # Ainda deleta para evitar retry infinito de mensagem mal formada
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                except InvalidAtivoError as iae:
                    logger.error(f"❌ Ativo inválido: {iae}", exc_info=True)
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

                except DatabaseError as dbe:
                    logger.error(f"❌ Erro ao acessar banco de dados: {dbe}", exc_info=True)
                    # Não deleta para retry posterior

                except TradingAnalysisError as tae:
                    logger.error(f"❌ Erro ao analisar trading: {tae}", exc_info=True)
                    # Não deleta para retry posterior

                except Exception as process_err:
                    logger.error(
                        f"❌ Erro inesperado ao processar mensagem: {process_err}",
                        exc_info=True
                    )
                    # Não deleta para retry posterior

        except ReadTimeoutError:
            logger.warning("⏱️ ReadTimeout na fila: sem resposta, tentando novamente...")

        except ClientError as e:
            logger.error(f"❌ Erro AWS SQS: {e.response['Error']['Code']}", exc_info=True)
            time.sleep(5)  # Pequeno delay antes de retry

        except Exception as e:
            logger.error(f"❌ Erro crítico ao consumir mensagens: {e}", exc_info=True)
            time.sleep(5)  # Pequeno delay para evitar loop rápido

        time.sleep(30)


def processar_persistencia(ativo):
    snapshot = SnapshotAcao(ativo)
    logger.info(f" Iniciando persistencia do objeto: : {snapshot}")
    db = SessionLocal()
    persistencia_service.registrar_snapshot(db, snapshot)


def processar_info(ativo):
    # gerar_insights(ativo)
    insight_single(ativo)


def insight_single(ativo):
    trading = TradingService()
    decisao, indicadores, insights = trading.processar_ativo(ativo)
    logger.info(f"🟢 Decisão: {decisao}")
    logger.info(f"🔣 Indicadores: {indicadores}")
    logger.info(f"💡 Insights: {insights}")
