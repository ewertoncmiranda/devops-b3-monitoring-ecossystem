from sqlalchemy.orm import Session

from app.config.config_logger import setup_logger
from app.external.database.historico_acao import HistoricoAcao
logger = setup_logger()


class HistoricoRepository:

    def salvar(self, db: Session, entidade: HistoricoAcao):
        logger.info(f" Iniciando salvar  : {entidade}")
        db.add(entidade)
        db.commit()
        db.refresh(entidade)
        logger.info(f" Objeto salvo  : {entidade}")
        return entidade
