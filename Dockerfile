FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including supervisor
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create supervisor configuration
RUN echo "[supervisord]\nnodaemon=true\n\n[program:fastapi]\ncommand=uvicorn app.main:app --host 0.0.0.0 --port 8000\n\n[program:streamlit]\ncommand=streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0" > /etc/supervisor/conf.d/services.conf

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"] 