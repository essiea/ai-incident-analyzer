terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

locals {
  lambda_name = "ai-incident-analyzer"
}

resource "aws_iam_role" "lambda_role" {
  name = "${local.lambda_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action   = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${local.lambda_name}-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = ["sns:Publish"]
        Resource = aws_sns_topic.incident_topic.arn
      }
    ]
  })
}

resource "aws_sns_topic" "incident_topic" {
  name = "ai-incident-analyzer-topic"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/../build/lambda.zip"
}

resource "aws_lambda_function" "ai_incident" {
  function_name = local.lambda_name
  role          = aws_iam_role.lambda_role.arn
  filename      = data.archive_file.lambda_zip.output_path
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 60

  environment {
    variables = {
      BEDROCK_MODEL_ID      = var.bedrock_model_id
      SNS_TOPIC_ARN         = aws_sns_topic.incident_topic.arn
      LOG_MAX_CHARS         = "8000"
      SUMMARY_MAX_TOKENS    = "350"
    }
  }
}

resource "aws_lambda_permission" "allow_logs" {
  statement_id  = "AllowExecutionFromCloudWatchLogs"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ai_incident.function_name
  principal     = "logs.${var.region}.amazonaws.com"
  source_arn    = "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:${var.source_log_group_name}:*"
}

resource "aws_cloudwatch_log_subscription_filter" "logs_sub" {
  name            = "ai-incident-analyzer-sub"
  log_group_name  = var.source_log_group_name
  filter_pattern  = ""
  destination_arn = aws_lambda_function.ai_incident.arn

  depends_on = [aws_lambda_permission.allow_logs]
}
