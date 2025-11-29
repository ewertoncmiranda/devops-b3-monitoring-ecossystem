import logging
import os
import time

from config import ensure_queue, ensure_dynamodb_table

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

def main():
    queue_name_insights = os.getenv('QUEUE_NAME_INSIGHTS', 'tratar-insights')
    queue_name = os.getenv('QUEUE_NAME', 'tratar-ativos')
    dynamo_table = os.getenv('DYNAMODB_NAME', 'infro-bruta-ativos-dynamodb')

    log.info("🔁 Verificando/Inicializando recursos AWS no LocalStack...")

    try:
        queue_url = ensure_queue(queue_name)
        log.info(f"✅ Fila pronta: {queue_url}")
    except Exception as e:
        log.error(f"❌ Erro ao verificar/criar fila: {e}")

    try:
        table_info = ensure_dynamodb_table(dynamo_table)
        log.info(f"✅ Tabela pronta: {table_info.get('TableName')}")
    except Exception as e:
        log.error(f"❌ Erro ao verificar/criar tabela: {e}")

    try:
        queue_url = ensure_queue(queue_name_insights)
        log.info(f"✅ Fila pronta: {queue_url}")
    except Exception as e:
        log.error(f"❌ Erro ao verificar/criar fila: {e}")

if __name__ == "__main__":
    while True:
        main()
        log.info("⏳ Aguardando 1 minutos para próxima execução...")
        time.sleep(60 * 1)
