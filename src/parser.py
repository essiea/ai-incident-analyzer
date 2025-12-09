import base64
import gzip
import json
from typing import Dict, Any


def decode_cloudwatch_logs_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Decode a CloudWatch Logs subscription event into JSON."""
    if "awslogs" not in event or "data" not in event["awslogs"]:
        raise ValueError("Invalid CloudWatch Logs event format")

    compressed_payload = base64.b64decode(event["awslogs"]["data"])
    decompressed = gzip.decompress(compressed_payload).decode("utf-8")
    logs = json.loads(decompressed)
    return logs


def format_logs_for_prompt(logs: Dict[str, Any]) -> str:
    """
    Format logs into a plain-text block for LLM consumption.
    """
    log_events = logs.get("logEvents", [])
    lines = []
    for e in log_events:
        ts = e.get("timestamp")
        msg = e.get("message", "").strip()
        lines.append(f"[{ts}] {msg}")
    return "\n".join(lines)
