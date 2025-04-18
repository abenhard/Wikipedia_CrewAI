import sys
import os
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from wikipedia_crewai.src.wikipedia_crewai.crew import WikipediaCrewai
from wikipedia_crewai.src.wikipedia_crewai.utils.topic_validator import validar_topico
from wikipedia_crewai.src.wikipedia_crewai.models import APIResponse, GeneratedArticle
from datetime import datetime

from typing import Optional

# Ajuste do caminho para módulos locais
BASE_DIR = os.path.dirname(__file__)
CREWAI_SRC_PATH = os.path.join(BASE_DIR, "wikipedia_crewai", "src")
if CREWAI_SRC_PATH not in sys.path:
    sys.path.insert(0, CREWAI_SRC_PATH)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = FastAPI()
crew = WikipediaCrewai()
# Arquivos estáticos, tools e templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
wikipedia_agent = WikipediaCrewai()
# Armazenamento simples de sessão
sessions = {}

class TopicRequest(BaseModel):
    topic: str
    current_year: Optional[str] = None

def run_crewai_workflow(inputs: dict):
    return wikipedia_agent.run(topic=inputs["topic"])

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Interface principal de chat"""
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
    """Processa pergunta do usuário e gera resposta"""
    if session_id not in sessions:
        return RedirectResponse(url="/")

    sessions[session_id]["messages"].append({
        "type": "user",
        "content": question
    })

    try:
        valido, resultado = validar_topico(question)
        if not valido:
            sugestoes = "\n".join(f"- {s}" for s in resultado)
            resposta = f"❌ O tópico é ambíguo ou não foi encontrado, seja mais especifico. Aqui estão algumas sugestões:\n{sugestoes}"
        else:
            inputs = {
                'topic': question,
                'current_year': str(datetime.now().year)
            }
            article = run_crewai_workflow(inputs)
            resposta = article.content

        sessions[session_id]["messages"].append({
            "type": "ai",
            "content": resposta
        })

    except Exception as e:
        sessions[session_id]["messages"].append({
            "type": "error",
            "content": f"Ocorreu um erro: {str(e)}"
        })

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "session_id": session_id,
        "messages": sessions[session_id]["messages"]
    })

@app.post("/api/ask", response_model=APIResponse)
async def api_ask(request: TopicRequest):
    """API pública para chamadas AJAX"""
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"messages": []}

    try:
        valido, resultado = validar_topico(request.topic)
        if not valido:
            return APIResponse(
                status="ambiguous",
                message="O tópico é ambíguo ou não foi encontrado, por favor seja mais específico.",
                suggestions=resultado if isinstance(resultado, list) else [],
                session_id=session_id
            )

        inputs = {
            'topic': request.topic,
            'current_year': request.current_year or str(datetime.now().year)
        }
        article = run_crewai_workflow(inputs)

        return APIResponse(
            status="success",
            message="Artigo gerado com sucesso",
            data={
                "article": {
                    "content": article.content,
                    "topic": article.topic,
                    "source_url": article.source_url,
                    "word_count": article.word_count
                }
            },
            session_id=session_id
        )

    except Exception as e:
        return APIResponse(
            status="error",
            message=f"Ocorreu um erro ao processar sua solicitação: {str(e)}",
            session_id=session_id
        )