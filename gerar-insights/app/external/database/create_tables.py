from app.config.database_config import engine
from app.external.database.historico_acao import Base

def criar_tabelas():
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Criação de tabelas concluida !")
