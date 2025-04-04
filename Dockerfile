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
RUN echo "[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:fastapi]\n\
command=uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/fastapi.err.log\n\
stdout_logfile=/var/log/fastapi.out.log\n\
\n\
[program:streamlit]\n\
command=streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/streamlit.err.log\n\
stdout_logfile=/var/log/streamlit.out.log" > /etc/supervisor/conf.d/services.conf

# Create log directory
RUN mkdir -p /var/log

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"] 