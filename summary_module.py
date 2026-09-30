from gemini_config import get_gemini_client

def get_summary(text: str) -> str:
    try:
        client = get_gemini_client()
        prompt = f"Summarize the following text clearly and concisely:\n\n{text}"
        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error in summarization: {str(e)}"
