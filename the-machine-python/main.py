from app.config.config import QUEUE_NAME
from app.external.sqs_service import ensure_queue
from app.external.sqs_service import consume_messages

def main():
    queue_url = ensure_queue(QUEUE_NAME)
    consume_messages(queue_url)

if __name__ == "__main__":
    main()
