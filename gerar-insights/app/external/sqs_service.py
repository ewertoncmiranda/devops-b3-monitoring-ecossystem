import json
import time
from datetime import datetime

from botocore.exceptions import ClientError, ReadTimeoutError
from app.config.config_logger import setup_logger
from app.config.aws_config import sqs
from app.external.dynamo_service import salvar_insights_em_dynamodb
from app.core.insights import gerar_insights
logger = setup_logger()

def ensure_queue(name: str) -> str:
    try:
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
                    logger.info(f"📈 Processando ativo: {ativo['symbol']}")

                    insights = gerar_insights(ativo)
                    salvar_insights_em_dynamodb(ativo, insights)

                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=m['ReceiptHandle'])

                except Exception as process_err:
                    logger.error(f"Erro ao processar mensagem específica: {process_err}", exc_info=True)

        except ReadTimeoutError:
            logger.warning("ReadTimeout: sem resposta, tentando novamente...")
        except ClientError as e:
            logger.error(f"AWS ClientError: {e}", exc_info=True)
        except Exception:
            logger.error("Erro ao consumir mensagens", exc_info=True)

        time.sleep(1)
