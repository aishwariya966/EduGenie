import google.generativeai as genai

def get_qna_answer(question: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model.generate_content(f"Answer this question: {question}").text
