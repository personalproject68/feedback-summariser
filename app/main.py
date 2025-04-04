from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from app.supabase import supabase
import os
import requests
from typing import List
from datetime import datetime

app = FastAPI()

class Feedback(BaseModel):
    name: str
    message: str

class SummarizeRequest(BaseModel):
    feedback: List[str]

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

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.post("/summarize")
async def summarize_feedback(request: SummarizeRequest = None):
    # Check if API key is set
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY in .env file."
        )
    
    try:
        # Fetch all feedback from Supabase
        print("Fetching all feedback from Supabase")
        feedback_data = supabase.table("feedback").select("*").execute()
        
        if not feedback_data.data:
            raise HTTPException(
                status_code=400,
                detail="No feedback found in the database"
            )
        
        # Extract and clean messages from feedback
        feedback_messages = []
        for item in feedback_data.data:
            message = item.get("message", "").strip()
            # Skip empty messages or test messages
            if (message and 
                not message.lower().startswith("test") and 
                not "supabase connection" in message.lower() and
                len(message) > 5):  # Skip very short messages
                feedback_messages.append(message)
        
        if not feedback_messages:
            raise HTTPException(
                status_code=400,
                detail="No valid feedback messages found after filtering test messages"
            )
        
        if len(feedback_messages) > 100:
            raise HTTPException(
                status_code=400,
                detail="Too many feedback messages. Maximum 100 messages allowed."
            )
        
        # Prepare the prompt with a better structure
        prompt = """Analyze these feedback messages and provide a BRIEF summary:

{}

Format your response in these sections:
1. Key Points: 2-3 main takeaways
2. Sentiment: Overall user satisfaction (positive/neutral/negative)
3. Suggestions: 1-2 key improvements if any

Keep it very concise - no more than 4-5 lines total.""".format("\n".join([f"• {msg}" for msg in feedback_messages]))

        print(f"\n--- OpenRouter API Request ---")
        print(f"API Key (first 10 chars): {OPENROUTER_API_KEY[:10]}...")
        print(f"Number of valid feedback messages: {len(feedback_messages)}")
        
        # Make the API request
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Feedback Summary App"
        }
        payload = {
            "model": "mistralai/mixtral-8x7b",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a concise feedback analyst. Keep summaries brief and to the point, focusing only on the most important insights."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # Lower temperature for more focused responses
            "max_tokens": 250    # Limit length to ensure conciseness
        }
        
        print("\n--- Making OpenRouter API Request ---")
        print(f"Headers: {headers}")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n--- OpenRouter API Response ---")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"OpenRouter API returned error: {response.text}"
            )
        
        response_json = response.json()
        if "choices" not in response_json or not response_json["choices"]:
            raise HTTPException(
                status_code=500,
                detail="OpenRouter API returned no choices in response"
            )
            
        summary = response_json["choices"][0]["message"]["content"]
        print(f"\n--- Generated Summary ---")
        print(summary)
        
        try:
            # Save summary to Supabase
            supabase_response = supabase.table("summaries").insert({
                "summary": summary,
                "feedback_count": len(feedback_messages),
                "created_at": datetime.utcnow().isoformat(),
                "feedback_messages": feedback_messages
            }).execute()
            
            print(f"\n--- Supabase Response ---")
            print(f"Status Code: {getattr(supabase_response, 'status_code', 'N/A')}")
            print(f"Response: {supabase_response}")
            
            return {
                "status": "success",
                "summary": summary,
                "feedback_count": len(feedback_messages)
            }
        except Exception as e:
            print(f"\n--- Supabase Error ---")
            print(f"Error: {str(e)}")
            # Even if saving to Supabase fails, return the summary to the user
            return {
                "status": "success",
                "summary": summary,
                "feedback_count": len(feedback_messages),
                "warning": "Summary generated but failed to save to database"
            }
            
    except requests.exceptions.Timeout:
        print("\n--- Error: Timeout ---")
        raise HTTPException(
            status_code=504,
            detail="Request to OpenRouter API timed out"
        )
    except requests.exceptions.ConnectionError:
        print("\n--- Error: Connection Error ---")
        raise HTTPException(
            status_code=503,
            detail="Failed to connect to OpenRouter API"
        )
    except requests.exceptions.RequestException as e:
        print(f"\n--- Error: Request Exception ---")
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"OpenRouter API request failed: {str(e)}"
        )
    except Exception as e:
        print(f"\n--- Error: Unexpected Exception ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/summaries")
async def get_summaries():
    try:
        print("Fetching summaries from Supabase")
        data = supabase.table("summaries").select("*").order("created_at", desc=True).execute()
        print(f"Retrieved {len(data.data)} summaries from Supabase")
        return {
            "status": "success",
            "count": len(data.data),
            "summaries": data.data
        }
    except Exception as e:
        print(f"Error fetching summaries from Supabase: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 