# AI Coding Agent

This project is an AI coding agent that helps with various coding tasks.

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
