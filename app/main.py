from fastapi import FastAPI
from pydantic import BaseModel
from app.supabase_client import supabase

app = FastAPI()

# Global storage for feedback
feedback = []

class FeedbackRequest(BaseModel):
    name: str
    message: str

@app.get("/hello")
async def hello():
    return {"message": "Hi, I'm alive"}

@app.get("/ping")
async def ping():
    return "pong"

@app.post("/submit")
def submit_feedback(data: FeedbackRequest):
    response = supabase.table("feedback").insert({
        "name": data.name,
        "message": data.message
    }).execute()

    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to insert into database")

    return {"status": "success", "data": response.data}

@app.get("/messages")
def get_messages():
    response = supabase.table("feedback").select("*").order("created_at", desc=True).execute()

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from database")

    return {"status": "success", "count": len(response.data), "messages": response.data}
