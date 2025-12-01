import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def wait_for_mysql(engine, retries=20, delay=7):
    for attempt in range(1, retries+1):
        try:
            print(f"Temtando conectar com MySQL : tentativa {attempt})")
            with engine.connect():
                print(f"MySQL está pronto (tentativa {attempt})")
                return
        except OperationalError:
            print(f"MySQL indisponível (tentativa {attempt}). Aguardando {delay}s...")
            time.sleep(delay)
    raise Exception("MySQL não respondeu no tempo esperado.")
