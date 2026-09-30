from gemini_config import get_gemini_client

def get_qna_answer(question: str) -> str:
    try:
        client = get_gemini_client()
        response = client.models.generate_content(model="gemini-3.8-flash", contents=question)
        return response.text.strip()
    except Exception as e:
        return f"Error in Q&A: {str(e)}"
