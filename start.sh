#!/bin/bash

# Function to cleanup background processes
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p)
    exit 0
}

# Trap SIGTERM and SIGINT
trap cleanup SIGTERM SIGINT

# Start FastAPI
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit
echo "Starting Streamlit..."
streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $? 