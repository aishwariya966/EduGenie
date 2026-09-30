from gemini_config import get_gemini_client

def get_quiz(topic: str) -> str:
    try:
        client = get_gemini_client()
        prompt = f"Generate 3 multiple-choice quiz questions on '{topic}'. Each question should have 4 options and mention the correct answer clearly at the end."
        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error in quiz generation: {str(e)}"
