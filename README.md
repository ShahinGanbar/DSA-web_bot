Web-bot: Interactive Data Analysis Assistant 🤖

A Streamlit-based web application that provides an intelligent data analysis assistant powered by Google's Gemini AI. Upload your CSV datasets and get instant insights through natural language queries, automated code generation, and interactive visualizations—all running inside Docker.

✨ Features

📊 Smart Data Analysis: Ask questions about your data in natural language

🤖 AI-Powered Code Generation: Automatically generates Python code for data manipulation, statistics, and visualizations

📈 Auto-Rendering Plots: Supports Plotly and Matplotlib/Seaborn

🔒 Safe Code Execution: Runs generated code in a controlled environment

💾 Session Management: Maintains analysis history and data state

📋 Interactive UI: Clean, modern interface with expandable chat history

🚀 Quick Start (Docker)
Prerequisites

Docker & Docker Compose installed

Google Gemini API key

1️⃣ Clone the repository
git clone <your-repo-url>
cd Web-bot

2️⃣ Set up environment variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # if using OpenAI models

3️⃣ Build and run with Docker Compose
docker compose up --build


The first build may take a few minutes.

Your app will be available at: http://localhost:8501

✅ Streamlit, dependencies, and API keys are all configured inside the container.

4️⃣ Stopping the app
docker compose down


This stops the container and frees port 8501.

📁 Project Structure
Web-bot/
├── src/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── llm/
│   │   └── chain.py          # LLM chain management and prompts
│   └── utils/
│       └── data_utils.py     # Data utilities and code execution
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # This file

🔧 How It Works

Data Upload: Upload CSVs; pandas loads data and extracts schema.

Natural Language Queries: Ask questions; LLM decides whether to explain or generate code.

Code Generation & Execution: Python code runs safely; plots auto-render.

Session Management: Keeps your data state and history.

💡 Usage Examples

"What's the average value of numeric columns?"

"Create a correlation matrix heatmap"

"Filter rows where column X > 100"

"Show me a pairplot of the features"

🛡️ Safety Features

No direct file I/O

Controlled environment with limited system access

Auto-package management for missing dependencies

Graceful error handling

🔌 Configuration
Environment Variables

GOOGLE_API_KEY — Required for Gemini AI

OPENAI_API_KEY — Required if using OpenAI models

Docker Ports

8501:8501 (host:container) by default

🚧 Limitations

Currently supports CSV files only

Requires internet connection for LLM API calls

Large datasets may impact performance

🤝 Contributing

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push (git push origin feature/amazing-feature)

Open a Pull Request

📝 License

MIT License — see the LICENSE file for details.

🙏 Acknowledgments

Streamlit

Google Gemini

LangChain

Pandas

Plotly and Matplotlib