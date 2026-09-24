import google.generativeai as genai

def get_explanation(concept: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(f"Explain this concept clearly: {concept}").text
