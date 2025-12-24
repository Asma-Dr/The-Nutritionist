#Import Libraries
from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import streamlit as st
import os
from PIL import Image
import requests
import json 
import base64

IMAGE_OCR_KEY = os.getenv("IMAGE_OCR_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_ID = os.getenv("GROQ_MODEL_ID", "meta-llama/llama-4-maverick-17b-128e-instruct")



def call_groq_vision(prompt, image_bytes, model_id=None, max_tokens=1024):
    """Groq vision model for direct image OCR + analysis."""
    if model_id is None:
        model_id = GROQ_MODEL_ID  # llama-4-maverick-17b-128e-instruct
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")
    
    # Encode image to base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model_id,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        }],
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    
    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                        headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def input_image_setup(uploaded_file):
    # Simple helper to return raw bytes of the uploaded image
    if uploaded_file is not None:
        return uploaded_file.getvalue()
    raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="The Nutritionist")

st.header("The Nutritionist")
## No Gemini required — the app will use OCR or Groq depending on env vars.
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the calories")

input_prompt="""
You are an image-to-nutrition assistant. For the provided plate image:

Detect and list each distinct food item (common name). If uncertain, provide multiple candidate labels with confidences.
Estimate portion size in grams and/or common serving units (e.g., "1 donut", "70 g chips") and state the assumed weight if exact measurement is unavailable.
For each item give: calories (kcal), macros in grams (carbs_g, fat_g, protein_g), and a confidence score (0–1). Where uncertainty is high, give a plausible range (min–max).
Provide totals for calories and macros.
List assumptions (portion defaults, restaurant vs homemade, visible toppings, occlusions).
Provide concise, actionable recommendations (2–4 bullet swaps or portion-control tips) and one short health interpretation sentence.
Prefer conservative estimates when items are partially occluded.
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
Finally you can also mention whether the food is healthy, balanced or not healthy and what all additional food items can be added in the diet which are healthy.

"""

## If submit button is clicked

if submit:
    if uploaded_file is None:
        st.error('Please upload an image first')
    else:
        image_bytes = uploaded_file.getvalue()
        
        # Priority 1: Direct Groq vision (fastest, no OCR.space needed)
        if GROQ_API_KEY:
            try:
                st.info("Using Groq Vision (direct image OCR)...")
                groq_resp = call_groq_vision(input_prompt, image_bytes, GROQ_MODEL_ID)
                st.subheader('Groq Vision Analysis')
                st.write(groq_resp)
                st.success("✅ Complete!")
                st.stop()  # Exit early on success
            except Exception as e:
                st.warning(f'Groq Vision failed: {e}')
