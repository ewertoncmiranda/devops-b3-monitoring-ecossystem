from app.config.aws_config import QUEUE_NAME
from app.config.config_logger import setup_logger
from app.config.database_config import engine
from app.config.timeout_db_engine import wait_for_mysql
from app.entrypoint.entrypoint_sqs import ensure_queue
from app.entrypoint.entrypoint_sqs import consume_messages
from app.external.database.create_tables import criar_tabelas

logger = setup_logger()

def main():
    logger.info("Iniciando aplicação")
    print("Aguardando MySQL ficar pronto...")
    wait_for_mysql(engine)
    criar_tabelas()
    queue_url = ensure_queue(QUEUE_NAME)
    consume_messages(queue_url)


if __name__ == "__main__":
    main()
