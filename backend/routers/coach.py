from fastapi import APIRouter, HTTPException
from backend.models import CoachRequest, CoachResponse, TitleRequest, TitleResponse
import os
import requests

router = APIRouter()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Use a text-optimized model for the coach
GROQ_MODEL_ID = "llama-3.3-70b-versatile" 

SYSTEM_PROMPT = """
You are 'The Nutritionist Coach', an empathetic and knowledgeable AI health assistant.
Your goal is to help users make better food choices, understand their nutrition, and reach their goals (weight loss, muscle gain, etc.).
Keep answers concise, motivating, and actionable.
"""

@router.post("/coach/chat", response_model=CoachResponse)
async def chat_with_coach(request: CoachRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    current_prompt = SYSTEM_PROMPT
    if request.context_data:
        current_prompt += f"\n\nContext from recent food analysis: {request.context_data}"

    messages = [
        {"role": "system", "content": current_prompt}
    ]

    # Append conversation history
    # Limit to last 10 messages to save context window if needed, but 70b has decent context
    for msg in request.history:
        # Ensure role is valid (groq expects 'user', 'assistant', 'system')
        role = msg.get("role", "user")
        if role not in ["user", "assistant"]:
            role = "user"
        messages.append({"role": role, "content": msg.get("content", "")})

    messages.append({"role": "user", "content": request.message})
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": GROQ_MODEL_ID,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
        if not response.ok:
            print(f"Groq API Error: {response.status_code} - {response.text}")
            raise Exception(f"Provider Error: {response.text}")
            
        reply = response.json()['choices'][0]['message']['content']
        return CoachResponse(reply=reply)
        
    except Exception as e:
        print(f"Coach error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/coach/title", response_model=TitleResponse)
async def generate_title(request: TitleRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    # Debug: Print received history
    print(f"DEBUG: Generating title for history length: {len(request.history)}")
    if not request.history:
        return TitleResponse(title="New Conversation")

    # Construct prompt for title generation
    messages = [
        {"role": "system", "content": "Create a TINY title (MAXIMUM 3 words) for this chat. simple and direct. Example: 'Fish Macros', 'Pizza Calories'. Return ONLY the title."},
    ]
    
    # Add history (limit to first few messages to get the topic)
    for msg in request.history[:6]: 
        role = msg.get("role", "user")
        content = msg.get("content", "")
        messages.append({"role": role, "content": content})
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 20, # Reduced to force brevity
        "temperature": 0.5
    }
    
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
        if not response.ok:
            print(f"Groq Title Error: {response.text}")
            return TitleResponse(title="Nutrition Chat")
            
        data = response.json()
        print(f"DEBUG: Groq Title Response: {data}")
        
        title = data['choices'][0]['message']['content'].strip().strip('"').strip('.')
        
        # Force truncation if AI rambles
        if len(title.split()) > 4:
            title = " ".join(title.split()[:4])
        
        # Fallback if empty
        if not title:
            title = "Nutrition Chat"
            
        return TitleResponse(title=title)
        
    except Exception as e:
        print(f"Title Gen Exception: {e}")
        return TitleResponse(title="Nutrition Chat")
