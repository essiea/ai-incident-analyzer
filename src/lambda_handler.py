import json
import logging
import boto3

from .parser import decode_cloudwatch_logs_event, format_logs_for_prompt
from .bedrock_client import summarize_logs
from .config import LOG_MAX_CHARS, SNS_TOPIC_ARN

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_sns = boto3.client("sns")


def _publish_sns(subject: str, message: str):
    if not SNS_TOPIC_ARN:
        logger.info("SNS_TOPIC_ARN not set; skipping SNS publish")
        return
    _sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject[:100], Message=message)


def lambda_handler(event, context):
    try:
        logger.debug("Received event: %s", json.dumps(event))

        logs = decode_cloudwatch_logs_event(event)
        log_str = format_logs_for_prompt(logs)
        if len(log_str) > LOG_MAX_CHARS:
            log_str = log_str[-LOG_MAX_CHARS:]

        analysis = summarize_logs(log_str)

        logger.info("AI Incident Analysis:\n%s", analysis)

        _publish_sns(
            subject="AI Incident Analysis",
            message=analysis,
        )

        return {"statusCode": 200, "body": json.dumps({"analysis": analysis})}
    except Exception as exc:
        logger.exception("Error analyzing logs: %s", exc)
        return {"statusCode": 500, "body": json.dumps({"error": str(exc)})}
