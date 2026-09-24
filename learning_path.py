import google.generativeai as genai

def get_learning_path(topic: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(f"Provide learning roadmap for: {topic}").text
