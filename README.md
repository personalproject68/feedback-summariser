# Feedback Portal

A feedback management system built with FastAPI and Streamlit, featuring automatic feedback summarization using AI.

## Features

- Submit feedback through a user-friendly interface
- View all submitted feedback
- Generate AI-powered summaries of feedback
- View feedback summaries with original messages
- Integration with Supabase for data storage
- OpenRouter API integration for AI summaries

## Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- Database: Supabase
- AI: OpenRouter API (Mixtral-8x7B)
- Containerization: Docker

## Prerequisites

- Docker and Docker Compose
- Supabase account and project
- OpenRouter API key

## Environment Variables

Create a `.env` file with the following variables:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd feedback-portal
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```

4. Run the Streamlit app:
```bash
streamlit run app_ui.py
```

## Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Access the applications:
- FastAPI: http://localhost:8000
- Streamlit UI: http://localhost:8501

## API Endpoints

- `POST /submit`: Submit new feedback
- `GET /messages`: Get all feedback messages
- `POST /summarize`: Generate summary of feedback
- `GET /summaries`: Get all generated summaries

## Database Schema

### Feedback Table
- name: string
- message: string
- created_at: timestamp

### Summaries Table
- summary: string
- feedback_count: integer
- created_at: timestamp
- feedback_messages: json array
