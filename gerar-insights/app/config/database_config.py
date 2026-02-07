import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config_logger import setup_logger

logger = setup_logger()

# =====================
# Database Configuration (100% from .env)
# =====================
DB_DRIVER = os.getenv("DB_DRIVER", "mysql+pymysql")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "spring")
DB_PASS = os.getenv("DB_PASS", "spring123")
DB_NAME = os.getenv("DB_NAME", "minha_base")

# Build connection URL dynamically
DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.info("=" * 70)
logger.info("Database Configuration")
logger.info("=" * 70)
logger.info(f"  Driver: {DB_DRIVER}")
logger.info(f"  Host: {DB_HOST}")
logger.info(f"  Port: {DB_PORT}")
logger.info(f"  User: {DB_USER}")
logger.info(f"  Database: {DB_NAME}")
logger.info("=" * 70)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

logger.info("Database engine created successfully")





