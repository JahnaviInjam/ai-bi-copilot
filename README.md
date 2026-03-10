# AI Business Intelligence Copilot

AI-powered analytics assistant that converts natural language questions into SQL queries and generates visual insights.

## Tech Stack
- Python
- FastAPI
- Streamlit
- OpenAI API
- SQLite
- Plotly
- Docker

## Features
- Natural language → SQL query generation
- Interactive analytics dashboard
- Automated data visualization
- REST API backend
- Containerized deployment

## Run Locally

```bash
docker build -t ai-bi-copilot .
docker run -p 8000:8000 -p 8501:8501 --env-file .env ai-bi-copilot