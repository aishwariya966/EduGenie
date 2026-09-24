import google.generativeai as genai

def get_summary(text: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(f"Summarize in points: {text}").text
