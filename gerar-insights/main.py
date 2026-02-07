import sys
import os
from dotenv import load_dotenv

# =====================
# Environment Detection and Configuration Loading
# =====================
environment = os.getenv('ENVIRONMENT', '').lower()

if environment == 'docker':
    # Docker environment: load .env.docker
    env_file = 'env/.env.docker'
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"Loaded configuration from: {env_file} (Environment: DOCKER)")
    else:
        print(f"Warning: Configuration file not found: {env_file}")
else:
    # Local environment: load .env.local
    env_file = '.env.local'
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"Loaded configuration from: {env_file} (Environment: LOCAL)")
    else:
        print(f"Warning: Configuration file not found: {env_file}")

from app.config.aws_config import QUEUE_NAME
from app.config.config_logger import setup_logger
from app.config.database_config import engine
from app.config.timeout_db_engine import wait_for_mysql, DatabaseConnectionError
from app.entrypoint.entrypoint_sqs import consume_messages
from app.entrypoint.entrypoint_sqs import ensure_queue
from app.external.database.config.create_tables import criar_tabelas

logger = setup_logger()


def main():
    try:
        logger.info("=" * 70)
        logger.info("Starting asset processing application")
        logger.info("=" * 70)

        logger.info("Checking database connection")
        wait_for_mysql(engine)

        logger.info("Creating database tables")
        criar_tabelas()

        logger.info(f"Validating SQS queue: {QUEUE_NAME}")
        queue_url = ensure_queue(QUEUE_NAME)
        logger.info(f"SQS queue validated: {queue_url}")

        logger.info("Starting message consumption")
        consume_messages(queue_url)

    except DatabaseConnectionError as e:
        logger.critical(f"Critical database connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Critical initialization error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()




