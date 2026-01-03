from sqlalchemy.orm import Session
from app.config.database_config import SessionLocal
from app.external.database.entity.historico_entity import HistoricoAcaoEntity
from app.external.database.entity.ativos_entity import AtivoEntity


class DatabaseService:

    def get_all_symbols(self) -> list[str]:
        db: Session = SessionLocal()
        try:
            rows = db.query(AtivoEntity.symbol).distinct().all()
            return [r[0] for r in rows]
        finally:
            db.close()

    def get_last_n_registros_ativos(self, symbol: str, n: int = 30):
        db = SessionLocal()
        try:
            return (
                db.query(AtivoEntity)
                .filter(AtivoEntity.symbol == symbol)
                .order_by(AtivoEntity.id.desc())
                .limit(n)
                .all()
            )
        finally:
            db.close()

    def get_latest_snapshot(self, symbol: str):
        db: Session = SessionLocal()
        try:
            return (
                db.query(AtivoEntity)
                  .filter(AtivoEntity.symbol == symbol)
                  .order_by(AtivoEntity.id.desc())
                  .first()
            )
        finally:
            db.close()
