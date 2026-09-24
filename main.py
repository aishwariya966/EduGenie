import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="EduGenie API")

# Configure Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_COPIED_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

class RequestModel(BaseModel):
    task: str  # Options: Explain, QnA, Quiz, Summary, Recommend Path
    user_input: str

@app.get("/")
def home():
    return {"message": "EduGenie Learning Assistant Backend is running!"}

@app.post("/generate")
def generate_response(data: RequestModel):
    task = data.task
    user_input = data.user_input

    # Task Specific Prompt Engineering
    if task == "Explain":
        prompt = f"Explain the following academic concept in detail with clear examples for a student:\n{user_input}"
    elif task == "QnA":
        prompt = f"Answer the following question concisely and accurately:\n{user_input}"
    elif task == "Quiz":
        prompt = f"Generate 3 multiple-choice questions (MCQs) with 4 options each and indicate the correct answer for the following topic:\n{user_input}"
    elif task == "Summary":
        prompt = f"Summarize the following text clearly in concise bullet points:\n{user_input}"
    elif task == "Recommend Path":
        prompt = f"Provide a step-by-step personalized learning path from beginner to advanced level with recommended resources for:\n{user_input}"
    else:
        prompt = user_input

    try:
        response = model.generate_content(prompt)
        return {
            "status": "success",
            "task": task,
            "result": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
