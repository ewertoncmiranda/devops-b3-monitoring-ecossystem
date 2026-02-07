import time
import os
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.config.config_logger import setup_logger

logger = setup_logger()

RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 10))


def wait_for_mysql(engine):
    """
    Wait for MySQL connection with configurable retry.

    Attempts RETRY_ATTEMPTS times with RETRY_DELAY seconds between each attempt.

    Args:
        engine: SQLAlchemy engine

    Raises:
        DatabaseConnectionError: If all attempts fail
    """
    total_wait_time = RETRY_ATTEMPTS * RETRY_DELAY

    logger.info("=" * 70)
    logger.info("Checking MySQL Connectivity")
    logger.info("=" * 70)
    logger.info(f"  Attempts: {RETRY_ATTEMPTS}")
    logger.info(f"  Interval: {RETRY_DELAY}s")
    logger.info(f"  Max total time: ~{total_wait_time}s")
    logger.info("=" * 70)

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            logger.info(f"\n[{attempt}/{RETRY_ATTEMPTS}] Connecting to MySQL...")
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("MySQL is ready and responding")
                logger.info("=" * 70)
                return
        except OperationalError as e:
            error_detail = str(e).split('\n')[0]
            logger.warning(f"Connection error: {error_detail}")

            if attempt < RETRY_ATTEMPTS:
                logger.info(f"Waiting {RETRY_DELAY}s before next attempt...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("All connection attempts failed")
                error_msg = (
                    f"\n{'=' * 70}\n"
                    f"CRITICAL: Database is unavailable\n"
                    f"{'=' * 70}\n"
                    f"MySQL did not respond after {RETRY_ATTEMPTS} attempts\n"
                    f"(with interval of {RETRY_DELAY}s each = ~{total_wait_time}s total)\n"
                    f"\nVerify:\n"
                    f"  - Environment variables (DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)\n"
                    f"  - MySQL container status: docker ps\n"
                    f"  - MySQL logs: docker logs mysql\n"
                    f"{'=' * 70}\n"
                )
                logger.critical(error_msg)
                raise DatabaseConnectionError(error_msg) from e


class DatabaseConnectionError(Exception):
    """Exception raised when database connection fails after retries."""
    pass

