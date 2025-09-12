# Web-bot: Interactive Data Analysis Assistant

A Streamlit-based web application that provides an intelligent data analysis assistant powered by Google's Gemini AI or OpenAI. Upload CSV datasets and get instant insights through natural language queries, automated code generation, and interactive visualizations.

## Features

* Smart Data Analysis – Ask questions about your data in natural language
* AI-Powered Code Generation – Automatically generates Pandas/NumPy/Plotly/Matplotlib code  
* Auto-Rendering Plots – Interactive visualizations with Plotly/Seaborn/Matplotlib
* Safe Code Execution – Runs generated code in a controlled environment
* Session Management – Persistent state with AWS DynamoDB (optional)
* Interactive UI – Clean, modern Streamlit interface
* AWS Integration – Containerized with Docker, deployed on ECS Fargate with ECR storage

## Quick Start

### Docker Deployment (Recommended)

**Prerequisites:**
* Docker & Docker Compose installed
* API key (Google Gemini)

**Steps:**

1. Clone the repository:
   ```bash
   git clone https://github.com/ShahinGanbar/Web-bot.git
   cd Web-bot
   ```

2. Create environment file:
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. Build and run:
   ```bash
   docker compose up --build
   ```

4. Access the application:
   Open your browser and navigate to `http://localhost:8501`

### Local Development

Only needed if you want to modify the code or prefer running without Docker.

**Prerequisites:**
* Python 3.10 
* API key (Google Gemini)

**Steps:**

1. Clone the repository:
   ```bash
   git clone https://github.com/ShahinGanbar/Web-bot.git
   cd Web-bot
   ```

2. Create and activate virtual environment:

   **Ubuntu/Linux/macOS:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file:
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run src/streamlit_app.py
   ```

6. Access the app at `http://localhost:8501`

## Ubuntu Setup

### For Docker Deployment

1. Update system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install Docker:
   ```bash
   sudo apt install docker.io docker-compose -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   ```

3. Build an image and run the container
   ```bash
   git clone https://github.com/ShahinGanbar/Web-bot.git
   cd Web-bot
   # Create .env file with your Gemini API key
   docker compose up --build
   ```

4. Follow the Docker deployment steps above

### For Local Development

If you need to modify the code:

1. Install Python:
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

2. Follow the local development steps above

## AWS Deployment

### Architecture Components

* **ECR (Elastic Container Registry)** - Stores Docker images securely
* **ECS (Fargate)** - Runs containerized app without server management
* **VPC & Security Groups** - Network configuration allowing traffic on port 8501
* **IAM Roles** - Access control for AWS services
* **Optional Services:**
  * S3 - Store and load CSV datasets
  * DynamoDB - Persistent session management
  * CloudWatch - Logging and monitoring
  * Secrets Manager - Secure API key storage

### Deployment Steps

1. Build and push Docker image to ECR
2. Create ECS cluster with Fargate launch type
3. Configure task definition with environment variables
4. Set up load balancer and security groups
5. Deploy and monitor through CloudWatch

## Project Structure

```
Web-bot/
├── app/
│   ├── __init__.py
│   └── main.py
├── llm/
│   ├── __init__.py
│   └── chain.py              # LLM chain logic and prompts
├── utils/
│   ├── __init__.py
│   └── data_utils.py         # Data utilities and safe execution
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .dockerignore            # Docker ignore file
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker image definition
├── compose.yaml            # Docker Compose configuration
├── README.md              # This file
├── README.Docker.md       # Docker-specific documentation
```

## Usage Examples

Try these natural language queries with your uploaded CSV data:

* "What's the average value of all numeric columns?"
* "Filter rows where sales > 1000 and show the top 10"
* "Create a correlation matrix heatmap"
* "Show me a scatter plot of price vs quantity"
* "Generate a pairplot of all features"
* "What are the unique values in the category column?"
* "Create a bar chart showing sales by region"

## Safety Features

* No Direct File I/O - Prevents unauthorized file system access
* Controlled Execution Environment - Code runs in isolated context
* Auto-Package Installation - Handles missing dependencies safely
* Error Handling - Clear feedback for execution issues
* Input Validation - Sanitizes user queries and data uploads

## Limitations

* Internet connection required for LLM API calls
* Large datasets (>100MB) may affect performance
* Generated code complexity depends on query specificity
* Rate limits apply based on your API provider

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and commit: `git commit -m "Add amazing feature"`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

* Add tests for new features
* Update documentation as needed
* Ensure Docker builds successfully

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* Streamlit - Web app framework
* Google Gemini / OpenAI - AI language models
* LangChain - LLM application framework
* Pandas, Plotly, Matplotlib - Data analysis and visualization
* AWS - Cloud infrastructure (ECS, ECR, VPC, IAM, CloudWatch)
