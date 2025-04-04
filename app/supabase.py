import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials in .env file")

print(f"Connecting to Supabase at: {supabase_url}")

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url=supabase_url,
    supabase_key=supabase_key
)

# Test the connection
try:
    # Try to get the feedback table info
    response = supabase.table("feedback").select("count").execute()
    print("Successfully connected to Supabase!")
except Exception as e:
    print(f"Error connecting to Supabase: {str(e)}") 