from app.config.aws_config import QUEUE_NAME
from app.config.config_logger import setup_logger
from app.external.sqs_service import ensure_queue
from app.external.sqs_service import consume_messages
logger = setup_logger()

def main():
    logger.info("Iniciando aplicação")
    queue_url = ensure_queue(QUEUE_NAME)
    consume_messages(queue_url)

if __name__ == "__main__":
    main()
