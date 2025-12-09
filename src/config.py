import os

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
LOG_MAX_CHARS = int(os.getenv("LOG_MAX_CHARS", "8000"))
SUMMARY_MAX_TOKENS = int(os.getenv("SUMMARY_MAX_TOKENS", "350"))
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")  # optional
