terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "aws_endpoint" {
  type        = string
  default     = "http://localhost:4566"
  description = "Endpoint para o LocalStack (mudar para http://localstack:4566 se rodar via Docker)"
}

# Configuração do Provider da AWS apontando para o LocalStack
provider "aws" {
  region     = "sa-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    sqs = var.aws_endpoint
  }
}

# ----------------------------------------------------
# SQS QUEUES
# ----------------------------------------------------
resource "aws_sqs_queue" "botafogo" {
  name                      = "botafogo"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    Environment = "local"
    Project     = "devops-b3-monitoring"
  }
}

resource "aws_sqs_queue" "tratar_ativos" {
  name                      = "tratar-ativos"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}
