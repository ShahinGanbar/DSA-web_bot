# Web-bot: Interactive Data Analysis Assistant 🤖

A Streamlit-based web application that provides an intelligent data analysis assistant powered by Google's Gemini AI. Upload your CSV datasets and get instant insights through natural language queries, automated code generation, and interactive visualizations.

## ✨ Features

- **📊 Smart Data Analysis**: Ask questions about your data in natural language
- **🤖 AI-Powered Code Generation**: Automatically generates Python code for data manipulation, statistics, and visualizations
- **📈 Auto-Rendering Plots**: Supports both Plotly and Matplotlib/Seaborn with automatic display
- **🔒 Safe Code Execution**: Runs generated code in a controlled environment with auto-package installation
- **💾 Session Management**: Maintains analysis history and data state throughout your session
- **📋 Interactive UI**: Clean, modern interface with expandable chat history

## 🚀 Quick Start

### Prerequisites

- Python 3.10
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
│   │   └── chain.py         # LLM chain management and prompts
│   └── utils/
│       └── data_utils.py    # Data utilities and code execution
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md               # This file
```

## 🔧 How It Works

### 1. Data Upload
- Upload CSV files through the web interface
- Data is loaded into memory as a pandas DataFrame
- Schema information (columns, dtypes, non-null counts) is extracted for LLM context

### 2. Natural Language Processing
- Ask questions about your data in plain English
- The LLM analyzes your request and decides whether to:
  - Provide an explanation (for conceptual questions)
  - Generate Python code (for computations, plots, transformations)

### 3. Intelligent Code Generation
- Code is generated based on your actual data structure
- Automatically handles imports and package installation
- Creates plots that render automatically in Streamlit

### 4. Safe Execution
- Generated code runs in a controlled environment
- Results are displayed with the current data state
- Analysis history is maintained for reference

## 💡 Usage Examples

### Ask Questions
- "What's the average value of numeric columns?"
- "Show me the correlation between features"
- "What are the data types of each column?"
- "Are there any missing values?"

### Request Analysis
- "Create a correlation matrix heatmap"
- "Plot the distribution of numeric columns"
- "Show me a pairplot of the features"
- "Calculate summary statistics"

### Data Transformations
- "Filter rows where column X > 100"
- "Group by category and calculate means"
- "Create a new column from existing ones"
- "Sort the data by a specific column"

## 🛡️ Safety Features

- **No File I/O**: Generated code cannot read/write files
- **Controlled Environment**: Code runs with limited access to system resources
- **Auto-Package Management**: Missing packages are automatically installed
- **Error Handling**: Graceful error handling with informative messages

## 🔌 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)

### LLM Settings
- Model: `gemini-1.5-flash`
- Temperature: Default (balanced creativity and accuracy)
- Max tokens: Handled automatically by the model

## 🚧 Limitations

- Currently supports CSV files only
- Requires internet connection for LLM API calls
- Generated code runs in the same process as the web app
- Large datasets may impact performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [Google Gemini](https://ai.google.dev/) for the AI capabilities
- [LangChain](https://langchain.com/) for LLM orchestration
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Plotly](https://plotly.com/) and [Matplotlib](https://matplotlib.org/) for visualizations

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/Web-bot/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Happy Data Analysis! 🎉**
