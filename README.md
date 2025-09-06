Web-bot: Interactive Data Analysis Assistant 🤖

A Streamlit-based web application that provides an intelligent data analysis assistant powered by Google's Gemini (or OpenAI). Upload CSV datasets and get instant insights through natural language queries, automated code generation, and interactive visualizations. Now deployed and scalable on AWS ECS (Fargate).

✨ Features

📊 Smart Data Analysis – Ask questions in natural language

🤖 AI-Powered Code Generation – Generates Pandas/NumPy/Plotly/Matplotlib code

📈 Auto-Rendering Plots – Interactive visualizations with Plotly/Seaborn/Matplotlib

🔒 Safe Code Execution – Runs code in a controlled environment

💾 Session Management – Persistent state with AWS DynamoDB (optional)

📋 Interactive UI – Clean, modern Streamlit interface

🚀 AWS Integration – Containerized with Docker, deployed on ECS Fargate, image stored in ECR, and secured with IAM roles.

Quick Start
Option 1: Run Locally

Prerequisites:

Python 3.10

Virtual environment (recommended)

API key (Google Gemini or OpenAI)

Installation:

git clone <repo-url>
cd Web-bot
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt


Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here # optional


Run the app:

streamlit run src/streamlit_app.py

Option 2: Run with Docker (Locally or on AWS)

Prerequisites:

Docker & Docker Compose installed

(Optional) AWS CLI configured for ECS/ECR deployment

Steps:

docker compose up --build


Access:

Local: http://localhost:8501

AWS ECS: http://(I'm sorry):8501

AWS Deployment Overview

ECR: Docker image stored in Amazon Elastic Container Registry.

ECS (Fargate): Runs the containerized Streamlit app without managing servers.

VPC & Security Groups: Configured to allow inbound traffic on port 8501.

IAM Roles:

ecsTaskExecutionRole allows ECS to pull images from ECR.

API keys stored securely via environment variables or AWS Secrets Manager.

Optional S3 Integration: Can store and load CSV datasets from Amazon S3 for scalability.

Optional DynamoDB: For persistent session management across multiple ECS tasks.

Monitoring: CloudWatch for logs and metrics.

Project Structure
Web-bot/
├── src/
│   ├── streamlit_app.py       # Main Streamlit application
│   ├── llm/
│   │   └── chain.py           # LLM chain logic and prompts
│   └── utils/
│       └── data_utils.py      # Data utilities and safe execution
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (created by user)
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # Documentation

Usage Examples

“What’s the average value of numeric columns?”

“Filter rows where column X > 100”

“Create a correlation matrix heatmap”

“Show me a pairplot of the features”

Safety Features

No direct file I/O

Controlled execution environment

Auto-installation of missing packages

Error handling with clear feedback

Limitations

Internet connection required for LLM API calls

Large datasets may affect performance

Contributing

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit (git commit -m "Add amazing feature")

Push (git push origin feature/amazing-feature)

Open a Pull Request

License

MIT License — see the LICENSE file.

Acknowledgments

Streamlit

Google Gemini / OpenAI

LangChain

Pandas, Plotly, Matplotlib

AWS (ECS, ECR, VPC, IAM, CloudWatch)
