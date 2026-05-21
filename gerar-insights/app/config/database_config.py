from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config_logger import setup_logger
from app.config.settings import Settings

logger = setup_logger()


class ConfigDatabase:
    def __init__(self):
        self.db = Settings().database_url
        self.engine = create_engine(
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        self.session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
