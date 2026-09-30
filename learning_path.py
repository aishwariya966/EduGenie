from gemini_config import get_gemini_client

def get_plan(topic: str) -> str:
    try:
        client = get_gemini_client()
        prompt = f"Create a step-by-step learning path for '{topic}' covering Beginner, Intermediate, and Advanced levels with estimated timelines and key subtopics."
        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error in learning path: {str(e)}"
