output "lambda_name" {
  value = aws_lambda_function.ai_incident.function_name
}

output "sns_topic_arn" {
  value = aws_sns_topic.incident_topic.arn
}
