from dataclasses import dataclass
from logging import Logger

from sqlalchemy.orm import Session

from app.external.database.entity.insight_entity import InsightEntity


@dataclass
class InsightRepository:

    def __init__(self, logger: Logger, db: Session):
        self.db = db
        self.logger = logger



    def salvar(self,entidade: InsightEntity):
        self.db.add(entidade)
        self.db.commit()
        self.db.refresh(entidade)
        self.logger.info(f"Insight para o ativo {entidade.simbolo} salvo no banco com sucesso.")
        return entidade
