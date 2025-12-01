import time

from botocore.exceptions import ClientError, ReadTimeoutError

from app.config.aws_config import sqs
from app.config.config_logger import setup_logger

logger = setup_logger()


def ensure_queue(name: str) -> str:
    try:
        logger.info(f"validando se fila sqs {name} existe:")
        logger.info(f"{sqs.list_queues()}")
        logger.info(f"{sqs.get_queue_url(QueueName=name)}")
        return sqs.get_queue_url(QueueName=name)['QueueUrl']

    except ClientError as e:
        logger.info(f"FILA {name} NÃO EXISTENTE")
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
                    # ativo = json.loads(mesg)
                    logger.info(f"📈 Processando mensagem : {mesg}")

                    # insights = gerar_insights(ativo)
                    # salvar_insights_em_dynamodb(ativo, insights)

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
