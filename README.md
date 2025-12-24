# 🥗 The Nutritionist

An AI-powered nutrition assistant that helps you analyze your meals and provides personalized coaching. Snap a photo of your food to get instant nutritional insights, and chat with your AI coach to reach your health goals.

## ✨ Features

- **📸 Instant Food Analysis**: Capture or upload a food image to get a detailed breakdown of calories, macronutrients (protein, carbs, fats), and a health score.
- **🤖 AI Nutrition Coach**: A conversational AI that offers diet advice, meal plans, and motivation.
- **🧠 Smart Conversation History**: 
  - Automatically saves your chat sessions.
  - **AI Title Generation**: Summarizes your conversations into short, catchy titles (e.g., "Keto Breakfast", "Pizza Calories").
  - Resume past conversations anytime from the history list.
- **📊 Meal History**: detailed log of all your analyzed meals.

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **AI Models**: 
  - Vision: Llama-3.2-11b-vision-preview (via Groq)
  - Chat/Coach: Llama-3.3-70b-versatile (via Groq)

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- A [Groq API Key](https://console.groq.com)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/TheNutritionist.git
cd TheNutritionist
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```ini
GROQ_API_KEY=gsk_your_api_key_here
```

## 🏃‍♂️ Running the Application

Start the backend server:

```bash
uvicorn backend.main:app --reload
```

The application will be available at: **http://127.0.0.1:8000**

## 📱 How to Use

1.  **Analyze Food**: Click the camera icon to take a picture of your meal (or upload one). The AI will analyze it and show you the nutritional data.
2.  **Chat with Coach**: Click the **Coach** button in the bottom navigation.
    - Ask questions like "Is this meal healthy?" or "Give me a 3-day detox plan".
    - **New Chat (+)**: Start a fresh conversation.
    - **History (List)**: View and resume your past chats. The titles are automatically generated for you!

## 📂 Project Structure

- `backend/`: FastAPI application code.
  - `routers/`: API endpoints for analysis and coach.
  - `services/`: Logic for interacting with Groq API.
- `frontend/`: Static files (HTML, CSS, JS).
- `test/`: Test scripts for verifying API functionality.

## 📄 License
MIT License
