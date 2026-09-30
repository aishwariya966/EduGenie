from gemini_config import get_gemini_client

def explain_topic(topic: str) -> str:
    try:
        client = get_gemini_client()
        prompt = f"Explain the concept of '{topic}' in simple, clear, and beginner-friendly terms."
        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error in explanation: {str(e)}"
