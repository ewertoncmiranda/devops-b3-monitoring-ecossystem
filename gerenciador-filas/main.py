import boto3
import os
import time

def verify_queue():
    # Load configuration from environment variables
    environment = os.environ.get('ENVIRONMENT', 'local')
    default_endpoint = 'http://localstack:4566' if environment == 'docker' else 'http://localhost:4566'
    
    endpoint_url = os.environ.get('LOCALSTACK_ENDPOINT', default_endpoint)
    region_name = os.environ.get('AWS_REGION', 'sa-east-1')
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', 'test')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', 'test')
    queue_name = os.environ.get('QUEUE_NAME', 'tratar-ativos')

    print(f"Connecting to LocalStack at {endpoint_url}...")
    
    sqs = boto3.client(
        'sqs',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    max_retries = 10
    for attempt in range(max_retries):
        try:
            print(f"Verifying if queue '{queue_name}' exists (Attempt {attempt + 1}/{max_retries})...")
            response = sqs.get_queue_url(QueueName=queue_name)
            print(f"Queue '{queue_name}' is ready. URL: {response.get('QueueUrl')}")
            break
        except Exception as e:
            print(f"Queue not found or error: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Max retries reached. Exiting.")
                raise

if __name__ == '__main__':
    verify_queue()
