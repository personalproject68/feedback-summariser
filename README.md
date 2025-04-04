# AI Coding Agent

This project is an AI coding agent that helps with various coding tasks.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Supabase credentials:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Running the FastAPI Server

To run the FastAPI server, use the following command:

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`. You can test the endpoints:

### GET /hello
- Visit `http://localhost:8000/hello` in your browser
- Or using curl: `curl http://localhost:8000/hello`

### GET /ping
- Visit `http://localhost:8000/ping` in your browser
- Or using curl: `curl http://localhost:8000/ping`

### GET /messages
View all submitted feedback:
```bash
curl http://localhost:8000/messages
```

### POST /submit
Submit feedback with name and message:
```bash
curl -X POST http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "message": "Great work!"}'
```

The API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Setup

The project uses Supabase for data storage. Make sure to:

1. Create a `feedback` table in your Supabase project with the following columns:
   - `id` (uuid, primary key)
   - `name` (text)
   - `message` (text)
   - `created_at` (timestamp with time zone, default: now())

2. Enable Row Level Security (RLS) if needed
3. Set up appropriate policies for the `feedback` table
