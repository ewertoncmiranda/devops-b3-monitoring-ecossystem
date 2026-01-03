import time

from sqlalchemy.exc import OperationalError


def wait_for_mysql(engine, retries=20, delay=60):
    for attempt in range(1, retries+1):
        try:
            print(f"Tentando conectar com MySQL : tentativa {attempt})")
            with engine.connect():
                print(f"MySQL está pronto (tentativa {attempt})")
                return
        except OperationalError:
            print(f"MySQL indisponível (tentativa {attempt}")
            time.sleep(delay)
    raise Exception("MySQL não respondeu no tempo esperado.")
