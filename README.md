# 🚨 AI Incident Analyzer (AWS + Bedrock)

![CI](https://github.com/essiea/ai-incident-analyzer/actions/workflows/ci.yml/badge.svg)  
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)  
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)  
![AWS](https://img.shields.io/badge/Cloud-AWS-orange)  
![License](https://img.shields.io/badge/License-MIT-green)

The **AI Incident Analyzer** is a serverless platform that consumes CloudWatch logs, decodes them, and uses **Amazon Bedrock (Claude 3 Sonnet)** to automatically produce:

- 📌 Human-readable summaries  
- ⚠️ Root cause analysis  
- 🔥 Severity classification  
- 🛠 Recommended remediation steps  
- 🔔 Optional SNS / Slack notifications  

This project brings **AI-driven observability** to DevOps/SRE workflows, reducing triage time and improving incident response.

---

## 🚀 Features

- Real-time CloudWatch → Lambda ingestion  
- Automatic decoding & parsing of AWS log payloads  
- Bedrock-powered natural language reasoning  
- Suggested fixes and severity scoring  
- SNS notification integration  
- Fully serverless architecture  
- Deployable entirely via Terraform  

---

## 🧠 Architecture

### Architecture Image

\`\`\`
docs/png/architecture.png
\`\`\`

### Mermaid Diagram

\`\`\`mermaid
flowchart TD
    CW[CloudWatch Logs] --> SF[Subscription Filter]
    SF --> L[Incident Analyzer Lambda]
    L --> B[Amazon Bedrock (Claude 3 Sonnet)]
    B --> L
    L --> SNS[(SNS Topic / Slack Webhook)]
\`\`\`

### ASCII View

\`\`\`
CloudWatch Logs → Subscription Filter → Lambda → Bedrock AI → SNS/Slack
\`\`\`

---

## 📁 Repository Structure

\`\`\`
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
\`\`\`

---

## 🔧 Requirements

- AWS account with **Bedrock enabled**  
- IAM permissions for:
  - Lambda  
  - CloudWatch Logs  
  - SNS  
  - \`bedrock:InvokeModel\`  
- Python **3.11**  
- Terraform **1.6+**  

---

## 🛠 Deployment (Terraform)

\`\`\`bash
cd terraform
terraform init
terraform apply -auto-approve \
  -var="source_log_group_name=/aws/lambda/my-api"
\`\`\`

---

## 🔥 Testing the Analyzer

\`\`\`json
{
  "awslogs": {
    "data": "<base64-gzip log payload>"
  }
}
\`\`\`

---

## 📤 Example Output

\`\`\`json
{
  "analysis": "### Summary...\\n### Root Cause...\\n### Severity: HIGH\\n### Recommended Fix..."
}
\`\`\`

---

## 💰 Cost Overview

| AWS Service       | Cost Estimate               |
|------------------|-----------------------------|
| Lambda           | pennies per month           |
| SNS              | generally free              |
| Bedrock          | free tier + minimal usage   |
| CloudWatch Logs  | standard ingestion pricing  |

---

## 🐛 Troubleshooting

| Issue                      | Fix                                                  |
|---------------------------|------------------------------------------------------|
| AccessDenied – Bedrock    | Add \`bedrock:InvokeModel\` to Lambda IAM role.        |
| Logs not analyzed         | Verify Subscription Filter is attached.              |
| SNS not sending           | Check \`SNS_TOPIC_ARN\` env variable.                  |
| Long logs truncated       | Adjust \`LOG_MAX_CHARS\` in config.py.                 |

---

## 🤝 Contributing  
PRs welcome.

---

## 📄 License  
MIT License.
