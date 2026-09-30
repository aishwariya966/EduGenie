import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Module Imports
from explanation_module import explain_topic
import qna
import quiz_module
import summary_module
import learning_path

app = FastAPI(title="EduGenie - AI Learning Assistant")

# Embedded HTML Design (No separate index.html file needed!)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduGenie</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f3f0fa;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
        }
        .container {
            background-color: #ffffff;
            width: 100%;
            max-width: 650px;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            text-align: center;
        }
        h1 { color: #1a1a1a; font-size: 26px; margin-bottom: 5px; }
        .subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
        .form-group { display: flex; gap: 10px; margin-bottom: 20px; }
        select { padding: 10px; border: 1px solid #ddd; border-radius: 8px; outline: none; background: #fff; }
        input[type="text"] { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; outline: none; }
        input[type="text"]:focus { border-color: #3b82f6; }
        button { background-color: #3b82f6; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
        button:hover { background-color: #2563eb; }
        .result-box { margin-top: 20px; text-align: left; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); display: none; }
        .result-title { font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #333; }
        .result-content { font-family: 'Courier New', Courier, monospace; font-size: 13px; color: #222; white-space: pre-wrap; line-height: 1.5; }
    </style>
</head>
<body>

<div class="container">
    <h1>Welcome to EduGenie 🧠✨</h1>
    <p class="subtitle">Your personal AI tutor for learning support!</p>

    <div class="form-group">
        <select id="moduleType">
            <option value="qna">Q&A</option>
            <option value="explanation">Explanation</option>
            <option value="summary">Summary</option>
            <option value="quiz">Quiz</option>
            <option value="learning path">Learning Path</option>
        </select>
        <input type="text" id="userInput" placeholder="Ask EduGenie a Question...">
        <button onclick="submitData()">Get Answer</button>
    </div>

    <div id="resultBox" class="result-box">
        <div class="result-title" id="resultTitle">Answer:</div>
        <div class="result-content" id="resultContent"></div>
    </div>
</div>

<script>
    async function submitData() {
        const input = document.getElementById("userInput").value;
        const type = document.getElementById("moduleType").value;
        const resultBox = document.getElementById("resultBox");
        const resultContent = document.getElementById("resultContent");
        const resultTitle = document.getElementById("resultTitle");

        if (!input) {
            alert("Please enter a question or topic!");
            return;
        }

        resultTitle.innerText = type.toUpperCase() + ":";
        resultContent.innerText = "Generating response...";
        resultBox.style.display = "block";

        try {
            const response = await fetch("/process", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ type: type, text: input })
            });

            const data = await response.json();
            resultContent.innerText = data.result || data.answer || data.explanation || "No response received.";
        } catch (error) {
            resultContent.innerText = "Error: Could not connect to backend server.";
        }
    }
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT

@app.post("/process")
async def process_request(request: Request):
    try:
        data = await request.json()
        task_type = str(data.get("type", "") or data.get("action", "") or data.get("module", "")).lower()
        input_text = str(data.get("text", "") or data.get("topic", "") or data.get("question", "")).strip()

        if not input_text:
            return JSONResponse(content={"result": "Dhayavuseidhu oru kelvi type pannungal."})

        res = ""
        if "qna" in task_type or "q&a" in task_type:
            res = qna.get_qna_answer(input_text)
        elif "explain" in task_type:
            res = explain_topic(input_text)
        elif "summa" in task_type:
            res = summary_module.get_summary(input_text)
        elif "quiz" in task_type:
            res = quiz_module.get_quiz(input_text)
        elif "learn" in task_type or "path" in task_type:
            res = learning_path.get_plan(input_text)
        else:
            res = qna.get_qna_answer(input_text)

        return JSONResponse(content={"result": res, "answer": res, "explanation": res})

    except Exception as e:
        return JSONResponse(content={"result": f"Server Error: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
