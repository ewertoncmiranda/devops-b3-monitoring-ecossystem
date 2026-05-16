from sqlalchemy.orm import Session
from app.config.config_logger import setup_logger
from app.external.database.entity.insight_entity import InsightEntity

logger = setup_logger()

class InsightRepository:

    def salvar(self, db: Session, entidade: InsightEntity):
        db.add(entidade)
        db.commit()
        db.refresh(entidade)
        logger.info(f"Insight para o ativo {entidade.simbolo} salvo no banco com sucesso.")
        return entidade
