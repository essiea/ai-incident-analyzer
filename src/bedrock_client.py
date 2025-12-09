import json
import boto3
from .config import MODEL_ID, SUMMARY_MAX_TOKENS

_bedrock = boto3.client("bedrock-runtime")


def summarize_logs(log_text: str) -> str:
    """
    Call Bedrock to summarize logs, identify root cause and remediation.
    """
    system_prompt = (
        "You are a senior SRE. Given application logs, you will:\n"
        "1) Summarize what happened.\n"
        "2) Identify probable root cause.\n"
        "3) Classify severity as LOW/MEDIUM/HIGH.\n"
        "4) Suggest clear remediation steps DevOps can execute.\n"
    )

    user_prompt = f"Here are the logs:\n\n{log_text}\n\nRespond in Markdown."

    body = {
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]},
        ],
        "max_tokens": SUMMARY_MAX_TOKENS,
        "temperature": 0.2,
    }

    response = _bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    payload = json.loads(response["body"].read())
    # Claude 3 format
    content = payload["output"]["message"]["content"]
    # content is a list of blocks; we join text segments
    text_parts = [c["text"] for c in content if c["type"] == "text"]
    return "\n".join(text_parts)
