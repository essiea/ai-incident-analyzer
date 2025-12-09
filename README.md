🚨 AI Incident Analyzer (AWS + Bedrock)










The AI Incident Analyzer is a serverless platform that consumes CloudWatch logs, decodes them, and uses Amazon Bedrock (Claude 3 Sonnet) to automatically produce:

📌 Human-readable summaries

⚠️ Root cause analysis

🔥 Severity classification

🛠 Recommended remediation steps

🔔 Optional SNS / Slack notifications

This project brings AI-driven observability to DevOps/SRE workflows, reducing triage time and improving incident response.

🚀 Features

Real-time CloudWatch → Lambda ingestion

Automatic decoding & parsing of AWS log payloads

Bedrock-powered natural language reasoning

Suggested fixes and severity scoring

SNS notification integration

Fully serverless architecture

Deployable entirely via Terraform

🧠 Architecture
📸 Architecture Image

(Generated automatically if you set up the diagram workflow.)

docs/png/architecture.png

🧩 Mermaid Diagram
flowchart TD
    CW[CloudWatch Logs] --> SF[Subscription Filter]
    SF --> L[Incident Analyzer Lambda]
    L --> B[Amazon Bedrock (Claude 3 Sonnet)]
    B --> L
    L --> SNS[(SNS Topic / Slack Webhook)]

🔎 ASCII View
CloudWatch Logs → Subscription Filter → Lambda → Bedrock AI → SNS/Slack

📁 Repository Structure
ai-incident-analyzer/
├── src/
│   ├── config.py
│   ├── parser.py
│   ├── bedrock_client.py
│   └── lambda_handler.py
└── terraform/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf

🔧 Requirements

AWS account with Bedrock enabled

IAM permissions for:

Lambda

CloudWatch Logs

SNS

bedrock:InvokeModel

Python 3.11

Terraform 1.6+

🛠 Deployment (Terraform)
cd terraform
terraform init
terraform apply -auto-approve \
  -var="source_log_group_name=/aws/lambda/my-api"


This deploys:

Lambda Analyzer

CloudWatch log subscription filter

Optional SNS topic

IAM execution role(s)

🔥 Testing the Analyzer (Lambda Console)

Use this sample event in the AWS Lambda Test UI:

{
  "awslogs": {
    "data": "<base64-gzip log payload>"
  }
}

📤 Example Output
{
  "analysis": "### Summary...\n### Root Cause...\n### Severity: HIGH\n### Recommended Fix..."
}

💰 Cost Overview
AWS Service	Cost Estimate
Lambda	pennies per month
SNS	generally free
Bedrock	free tier + minimal usage
CloudWatch Logs	standard ingestion pricing

This architecture is optimized to stay within the AWS Free Tier for light workloads.

🐛 Troubleshooting
Issue	Fix
AccessDenied – Bedrock	Add bedrock:InvokeModel to Lambda execution IAM role.
Logs not being analyzed	Verify CloudWatch → Log Subscription Filter is attached.
SNS notifications not firing	Ensure SNS_TOPIC_ARN is correctly set in environment vars.
Long logs being truncated	Adjust LOG_MAX_CHARS in src/config.py.
🤝 Contributing

Contributions, issues, and feature requests are welcome!
Open a PR or submit an issue to get involved.

📄 License

This project is licensed under the MIT License.
