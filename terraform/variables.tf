variable "region" {
  type    = string
  default = "us-east-1"
}

variable "source_log_group_name" {
  description = "CloudWatch log group name to subscribe (e.g. /aws/lambda/my-api)"
  type        = string
}

variable "bedrock_model_id" {
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
  description = "Bedrock Claude 3 Sonnet model ID"
}
