🚨 AI Incident Analyzer (AWS + Bedrock)










The AI Incident Analyzer is a serverless platform that consumes CloudWatch logs, decodes and processes them, and uses Amazon Bedrock (Claude 3 Sonnet) to automatically generate:

📌 Human-readable incident summaries

⚠️ Root cause analysis

🔥 Severity classification

🛠 Recommended remediation steps

🔔 Optional SNS / Slack notifications

This brings AI-driven observability into DevOps/SRE workflows to reduce triage time and accelerate incident resolution.

🚀 Features

Real-time ingestion from CloudWatch Log Groups

Automated decoding & transformation of AWS Logs

Bedrock LLM–powered analysis and recommendations

Pluggable notifications (SNS / Slack)

Fully serverless, low-cost, scalable architecture

100% IaC via Terraform

🧠 Architecture
Architecture Image

(Ensure docs/png/architecture.png exists from your GitHub Action auto-generator.)

Mermaid Diagram
flowchart TD
    CW[CloudWatch Logs] --> SF[Subscription Filter]
    SF --> L[Incident Analyzer Lambda]
    L --> B[Amazon Bedrock (Claude 3 Sonnet)]
    B --> L
    L --> SNS[(SNS Topic / Slack Webhook)]

ASCII View
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

Terraform ≥ 1.6

Python 3.11

🛠 Deployment (Terraform)
cd terraform
terraform init
terraform apply -auto-approve \
  -var="source_log_group_name=/aws/lambda/my-api"


This deploys:

Lambda Analyzer

CloudWatch log subscription filter

SNS topic (optional)

IAM roles

🔥 Testing the Analyzer (Lambda Console)

Use the AWS Lambda Test UI with a sample event:

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
AWS Service	Cost
Lambda	pennies per month
SNS	generally free
Bedrock	free tier + pay-per-use
CloudWatch Logs	standard log ingestion pricing

This architecture is optimized to stay within AWS Free Tier for light workloads.

🐛 Troubleshooting
Issue	Resolution
AccessDenied – Bedrock	Add bedrock:InvokeModel to the Lambda execution role.
Logs not being analyzed	Check CloudWatch → Subscription Filters configuration.
SNS notifications not sending	Verify the SNS_TOPIC_ARN environment variable.
Long logs truncated	Modify LOG_MAX_CHARS in config.py.
🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open a PR or submit an issue.

📄 License

This project is licensed under the MIT License.
