from config_infra import *
import os

def main():
    queue_name = os.getenv('QUEUE_NAME', 'themachine')
    dynamo_table = os.getenv('DYNAMODB_NAME', 'themachine-db')

    print("🔁 Verificando recursos AWS no LocalStack...")

    queue_url = ensure_queue(queue_name)
    print(f"✅ Fila ativa em: {queue_url}")

    table_info = ensure_dynamodb_table(dynamo_table)
    print(f"✅ Tabela ativa: {table_info.get('TableName')}")

if __name__ == "__main__":
    main()
