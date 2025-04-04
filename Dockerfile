FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Run both services using a shell command
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0 && fg 