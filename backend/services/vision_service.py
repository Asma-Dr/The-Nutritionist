import os
import requests
import base64
import json
from backend.models import AnalysisResponse, FoodItem, MacroNutrients

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "llama-3.2-90b-vision-preview") # Updated to a vision capable model if needed, otherwise user default

SYSTEM_PROMPT = """
You are an expert nutritionist and computer vision AI. 
Analyze the image of food provided. 
Return ONLY valid JSON matching this structure exactly:
{
  "food_items": [
    {
      "name": "string",
      "confidence": float (0-1),
      "portion_desc": "string (e.g. 1 cup, 2 slices)",
      "weight_g": float (estimated),
      "nutrition": {
        "calories_kcal": float,
        "protein_g": float,
        "carbs_g": float,
        "fat_g": float,
        "sugar_g": float,
        "fiber_g": float
      },
      "health_rating": "string (Healthy/Moderate/Unhealthy)"
    }
  ],
  "total_nutrition": {
    "calories_kcal": float,
    "protein_g": float,
    "carbs_g": float,
    "fat_g": float,
    "sugar_g": float,
    "fiber_g": float
  },
  "health_score": int (0-100),
  "health_summary": "string (1-2 sentences)",
  "recommendations": ["string", "string"],
  "warnings": ["string"]
}
Do not add any markdown formatting (like ```json), just the raw JSON string.
"""

from PIL import Image
import io

def analyze_image(image_bytes: bytes, media_type: str = "image/jpeg") -> AnalysisResponse:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set.")

    # Validate and Resize Image (Groq has limits and smaller is faster)
    try:
        img = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if needed (e.g. PNG with alpha)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize if dimension > 1024 to save tokens/bandwidth
        max_size = 1024
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size))
        
        # Save back to bytes as JPEG for consistency
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        processed_image_bytes = buffer.getvalue()
        media_type = "image/jpeg" # We converted to JPEG
    except Exception as e:
        print(f"Image processing error: {e}")
        # Fallback to original bytes if PIL fails
        processed_image_bytes = image_bytes

    base64_image = base64.b64encode(processed_image_bytes).decode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct", # Updated to new Llama 4 Multimodal
        "messages": [
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{media_type};base64,{base64_image}"}
                    }
                ]
            }
        ],
        "max_tokens": 2048,
        "temperature": 0.1,
        # "response_format": {"type": "json_object"} # Removed as it causes 400 on some vision models
    }
    
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=60)
        if not response.ok:
            print(f"Groq API Error: {response.status_code} - {response.text}")
        response.raise_for_status()
        
        content = response.json()['choices'][0]['message']['content']
        # Parse JSON
        data = json.loads(content)
        
        # Validate with Pydantic
        return AnalysisResponse(**data)
        
    except json.JSONDecodeError:
        # Fallback/Retry logic could go here, for now raise
        raise ValueError("Failed to parse JSON from AI response")
    except Exception as e:
        print(f"Error in vision service: {e}")
        raise e
