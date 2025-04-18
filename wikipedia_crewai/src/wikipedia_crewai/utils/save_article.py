from pathlib import Path
import re
from datetime import datetime

def get_project_root() -> Path:
    """Sobe 4 níveis a partir de utils/ para chegar na raiz do projeto"""
    current_path = Path(__file__).resolve()
    # utils -> wikipedia_crewai -> src -> wikipedia_crewai -> Wikipedia_CrewAI
    return current_path.parent.parent.parent.parent.parent

def save_article_to_file(topic: str, content: str):
    project_root = get_project_root()
    articles_dir = project_root / "artigos"  # Agora vai apontar para E:\Wikipedia_CrewAI\artigos
    articles_dir.mkdir(exist_ok=True)

    # Gera nome do arquivo seguro
    timestamp = datetime.now().strftime("%d-%m-%Y")
    safe_topic = re.sub(r'[^a-zA-Z0-9_-]', '_', topic.lower())
    base_filename = f"{safe_topic}_{timestamp}"
    filename = f"{base_filename}.md"
    filepath = articles_dir / filename

    # Controle de versões
    version = 1
    while filepath.exists():
        filename = f"{base_filename}_v{version}.md"
        filepath = articles_dir / filename
        version += 1

    filepath.write_text(content, encoding="utf-8")
    print(f"✅ Artigo salvo em: {filepath}")
    return str(filepath)