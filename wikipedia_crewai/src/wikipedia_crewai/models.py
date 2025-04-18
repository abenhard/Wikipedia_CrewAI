from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class GeneratedArticle(BaseModel):
    topic: str
    content: str
    word_count: int
    source_url: str
    reliability_flags: List[str] = []

class APIResponse(BaseModel):
    status: str  # "success", "error" ou "ambiguous"
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None  # Aqui será armazenado o artigo
    suggestions: Optional[List[str]] = None
    session_id: Optional[str] = None