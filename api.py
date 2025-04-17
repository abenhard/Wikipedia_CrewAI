import sys
import os
BASE_DIR = os.path.dirname(__file__)
CREWAI_SRC_PATH = os.path.join(BASE_DIR, "wikipedia_crewai", "src")
if CREWAI_SRC_PATH not in sys.path:
    sys.path.insert(0, CREWAI_SRC_PATH)

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from wikipedia_crewai.crew import WikipediaCrewai
from datetime import datetime
import uuid
import warnings
from typing import Optional

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="E:/Wikipedia_CrewAI/static"), name="static")
templates = Jinja2Templates(directory="E:/Wikipedia_CrewAI/templates")

# Session storage (use proper database in production)
sessions = {}


class TopicRequest(BaseModel):
    topic: str
    current_year: Optional[str] = None


def run_crewai_workflow(inputs: dict):
    return WikipediaCrewai().run(topic=inputs["topic"])


@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Main chat-like interface"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"messages": []}
    response = templates.TemplateResponse("chat.html", {
        "request": request,
        "session_id": session_id,
        "messages": []
    })
    response.set_cookie(key="session_id", value=session_id)
    return response


@app.post("/ask", response_class=HTMLResponse)
async def process_question(request: Request, question: str = Form(...), session_id: str = Form(...)):
    """Process user question and generate response"""
    if session_id not in sessions:
        return RedirectResponse(url="/")

    # Adicionando a pergunta do usuário à sessão
    sessions[session_id]["messages"].append({
        "type": "user",
        "content": question
    })

    try:
        # Processar com CrewAI
        inputs = {
            'topic': question,
            'current_year': str(datetime.now().year)
        }
        result = run_crewai_workflow(inputs)

        # Garantir que a resposta seja retornada corretamente
        sessions[session_id]["messages"].append({
            "type": "ai",
            "content": result  # Certifique-se de que 'result' é o conteúdo em Markdown ou HTML
        })
    except Exception as e:
        sessions[session_id]["messages"].append({
            "type": "error",
            "content": f"An error occurred: {str(e)}"
        })

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "session_id": session_id,
        "messages": sessions[session_id]["messages"]
    })


@app.post("/api/ask")
async def api_ask(request: TopicRequest):
    """API endpoint for AJAX requests"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"messages": []}

    try:
        inputs = {
            'topic': request.topic,
            'current_year': request.current_year or str(datetime.now().year)
        }
        result = run_crewai_workflow(inputs)

        return {
            "status": "success",
            "session_id": session_id,
            "response": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
