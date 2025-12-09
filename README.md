# 🚨 AI Incident Analyzer (AWS + Bedrock)

![CI](https://github.com/<YOUR_GITHUB_USERNAME>/ai-incident-analyzer/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)
![AWS](https://img.shields.io/badge/Cloud-AWS-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An **AI-powered incident analysis platform** that consumes CloudWatch logs, decodes and processes them, and uses **Amazon Bedrock (Claude 3 Sonnet)** to automatically generate:

- 📌 Human-readable summaries  
- ⚠️ Root cause analysis  
- 🔥 Severity classification  
- 🛠 Recommended remediation steps  
- 🔔 SNS / Slack notifications  

This project introduces LLM-augmented observability to improve DevOps/SRE response time and reduce manual triage.

---

## 🚀 Features

- Real-time CloudWatch → Lambda ingestion  
- Decoding + processing of log payloads  
- Bedrock-powered natural-language analysis  
- Root cause inference and fix suggestions  
- Serverless (very low-cost, scalable)  
- Deployable via Terraform  

---

## 🧠 Architecture

![Architecture](docs/png/architecture.png)

### Mermaid Diagram
```mermaid
flowchart TD
    CW[CloudWatch Logs] --> SF[Subscription Filter]
    SF --> L[Incident Analyzer Lambda]
    L --> B[Amazon Bedrock (Claude 3 Sonnet)]
    B --> L
    L --> SNS[(SNS Topic / Slack Webhook)]
ASCII View
pgsql
Copy code
CloudWatch Logs → Subscription Filter → Lambda → Bedrock AI → SNS/Slack
📁 Repository Structure
css
Copy code
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
AWS Account with Bedrock enabled

AWS IAM permissions for Lambda, CloudWatch Logs, SNS

Terraform ≥ 1.6

Python 3.11

🛠 Deployment (Terraform)
bash
Copy code
cd terraform
terraform init
terraform apply -auto-approve \
  -var="source_log_group_name=/aws/lambda/my-api"
🔥 Testing the Lambda
Use AWS Console → Lambda → Test, with:

json
Copy code
{
  "awslogs": { "data": "<base64-gzip log payload>" }
}
📤 Output Example
json
Copy code
{
  "analysis": "### Summary...\n### Root Cause...\n### Severity: HIGH...\n### Recommended Fix..."
}
💰 Cost Overview
AWS Service	Cost
Lambda	pennies per month
SNS	mostly free
Bedrock API	free tier + pay per request
CloudWatch Logs	standard ingest

🐛 Troubleshooting
Problem	Fix
Bedrock Access Denied	Add bedrock:InvokeModel permission
No logs being processed	Attach log subscription correctly
SNS notifications not firing	Ensure SNS_TOPIC_ARN is set

🤝 Contributing
PRs welcome! Please submit issues or enhancements.

📄 License
MIT License.
