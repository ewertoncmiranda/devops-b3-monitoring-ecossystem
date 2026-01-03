from app.config.database_config import engine
from app.external.database.entity.ativos_entity import Base as ativos
from app.external.database.entity.historico_entity  import Base as historico

def criar_tabelas():
    print("Criando tabelas...")
    historico.metadata.create_all(bind=engine)
    ativos.metadata.create_all(bind=engine)
    print("Criação de tabelas concluida !")
