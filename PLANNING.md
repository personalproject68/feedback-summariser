# Project Planning

This project is an AI coding agent starting with a simple FastAPI setup to validate the environment.

## Project Structure
- `main.py`: Contains the FastAPI application
- `README.md`: Documentation and setup instructions
- `TASK.md`: Task tracking and progress
- `PLANNING.md`: Project planning and architecture decisions

## Features
- Basic server setup with health check endpoints (/hello, /ping)
- Feedback submission system with POST /submit endpoint
  - Accepts name and message
  - Stores submissions in memory
  - Returns success response with submitted data
- Feedback retrieval system with GET /messages endpoint
  - Returns all submitted feedback
  - Includes count of total messages
  - Returns messages in chronological order
