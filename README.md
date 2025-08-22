Web-bot: Interactive Data Analysis Assistant 🤖

A Streamlit-based web application that provides an intelligent data analysis assistant powered by Google's Gemini (or OpenAI). Upload CSV datasets and get instant insights through natural language queries, automated code generation, and interactive visualizations.

✨ Features

📊 Smart Data Analysis – Ask questions in natural language

🤖 AI-Powered Code Generation – Generates Pandas/NumPy/Plotly/Matplotlib code

📈 Auto-Rendering Plots – Interactive visualizations with Plotly/Seaborn/Matplotlib

🔒 Safe Code Execution – Runs code in a controlled environment

💾 Session Management – Keeps state and history

📋 Interactive UI – Clean, modern Streamlit interface

🚀 Quick Start
Option 1: Run Locally
Prerequisites

Python 3.8+

Virtual environment (recommended)

API key (Google Gemini or OpenAI)

Installation
# Clone repository
git clone <your-repo-url>
cd Web-bot

# Create and activate venv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here   # optional(you can change llm in chain.py)


Run the app:

streamlit run src/streamlit_app.py

Option 2: Run with Docker
Prerequisites

Docker & Docker Compose installed

Steps
# Build and run
docker compose up --build


Visit: http://localhost:8501

📁 Project Structure
Web-bot/
├── src/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── llm/
│   │   └── chain.py          # LLM chain logic and prompts
│   └── utils/
│       └── data_utils.py     # Data utilities and safe execution
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (you create this)
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # Documentation

💡 Usage Examples

“What’s the average value of numeric columns?”

“Filter rows where column X > 100”

“Create a correlation matrix heatmap”

“Show me a pairplot of the features”

🛡️ Safety Features

No direct file I/O

Controlled execution environment

Auto-installation of missing packages

Error handling with clear feedback

🚧 Limitations

CSV input only (for now)

Internet connection required for LLM API calls

Large datasets may affect performance

🤝 Contributing

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit (git commit -m "Add amazing feature")

Push (git push origin feature/amazing-feature)

Open a Pull Request

📝 License

MIT License — see the LICENSE file.

🙏 Acknowledgments

Streamlit

Google Gemini / OpenAI

LangChain

Pandas, Plotly, Matplotlib
