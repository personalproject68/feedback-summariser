from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Global storage for feedback
feedback = []

class Feedback(BaseModel):
    name: str
    message: str

@app.get("/hello")
async def hello():
    return {"message": "Hi, I'm alive"}

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/submit")
async def submit_feedback(feedback_item: Feedback):
    feedback.append(feedback_item.dict())
    return {
        "status": "success",
        "message": "Feedback submitted successfully",
        "data": feedback_item.dict()
    }

@app.get("/messages")
async def get_messages():
    return {
        "status": "success",
        "count": len(feedback),
        "messages": feedback
    }
