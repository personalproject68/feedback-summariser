from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.supabase import supabase

app = FastAPI()

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
    try:
        print(f"Received feedback from {feedback_item.name}")
        # Insert feedback into Supabase
        data = supabase.table("feedback").insert({
            "name": feedback_item.name,
            "message": feedback_item.message
        }).execute()
        
        print(f"Successfully stored feedback in Supabase: {data.data}")
        return {
            "status": "success",
            "message": "Feedback submitted successfully",
            "data": data.data[0]
        }
    except Exception as e:
        print(f"Error storing feedback in Supabase: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages")
async def get_messages():
    try:
        print("Fetching messages from Supabase")
        # Get all feedback from Supabase
        data = supabase.table("feedback").select("*").execute()
        print(f"Retrieved {len(data.data)} messages from Supabase")
        return {
            "status": "success",
            "count": len(data.data),
            "messages": data.data
        }
    except Exception as e:
        print(f"Error fetching messages from Supabase: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 