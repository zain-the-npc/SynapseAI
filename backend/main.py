import os
import base64
from pathlib import Path  # Added for reliable path finding
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse 
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI

# 1. LOAD ENVIRONMENT VARIABLES (Updated for folder-specific loading)
# This finds the .env file in the SAME folder as this main.py file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. INITIALIZE CLIENT
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("CRITICAL WARNING: OPENAI_API_KEY is not set. Check your .env file.")

# Initialize client; we'll handle the missing key error gracefully in the endpoint
client = OpenAI(api_key=OPENAI_API_KEY or "MISSING_KEY")

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    image_base64: Optional[str] = None

SYSTEM_PROMPT = """
You are the "Paper-to-Brain" Intelligence Engine, an elite Academic Teaching Assistant.
Your purpose is to analyze STEM notes, PDFs, and complex assignments.

CRITICAL INSTRUCTION:
1. If a document or image contains multiple questions, you MUST answer EVERY single one in full detail.
2. Use LaTeX for all mathematical formulas.
3. Do not cut off your response. Provide exhaustive explanations.
"""

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Security check: verify key exists before calling OpenAI
    if not OPENAI_API_KEY or OPENAI_API_KEY == "MISSING_KEY":
        raise HTTPException(status_code=500, detail="OpenAI API Key is missing on the server.")

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Build conversation history
        for entry in request.history:
            messages.append({"role": entry["role"], "content": entry["content"]})
        
        # Prepare current user message
        user_content = [{"type": "text", "text": request.message}]
        
        # Handle Image Input if present
        if request.image_base64:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{request.image_base64}"}
            })
        
        messages.append({"role": "user", "content": user_content})

        # Generator function for real-time streaming
        def generate_chunks():
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages,
                max_tokens=4000,
                temperature=0.7,
                stream=True 
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return StreamingResponse(generate_chunks(), media_type="text/plain")

    except Exception as e:
        print(f"Backend Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")