Web-bot: Interactive Data Analysis Assistant 🤖

A Streamlit-based web application that provides an intelligent data analysis assistant powered by Google's Gemini AI. Upload your CSV datasets and get instant insights through natural language queries, automated code generation, and interactive visualizations—all running inside Docker.

✨ Features

📊 Smart Data Analysis: Ask questions about your data in natural language

🤖 AI-Powered Code Generation: Automatically generates Python code for data manipulation, statistics, and visualizations

📈 Auto-Rendering Plots: Supports Plotly and Matplotlib/Seaborn

🔒 Safe Code Execution: Runs generated code in a controlled environment

💾 Session Management: Maintains analysis history and data state

📋 Interactive UI: Clean, modern interface with expandable chat history

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Web-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run src/streamlit_app.py
   ```

## 📁 Project Structure

```
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