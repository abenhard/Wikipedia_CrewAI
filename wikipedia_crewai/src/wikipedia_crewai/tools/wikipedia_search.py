from crewai.tools import tool
import requests
from urllib.parse import quote
from typing import Dict, Any

@tool("wikipedia_search")
def wikipedia_search(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ferramenta que realiza a busca e extração de informações de um artigo da Wikipédia em português,
    com base em um tópico ou descrição fornecida no campo 'description'.
    """
    try:
        # Permitir chamadas diretas com {"description": "..."}, ou aninhadas com {"input_data": {"description": "..."}}
        if "input_data" in input_data:
            input_data = input_data["input_data"]

        topic = input_data.get("description", "").strip()

        if not topic:
            return {"erro": "Nenhum tópico válido fornecido"}

        base_url = "https://pt.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info|categories",
            "titles": topic,
            "explaintext": True,
            "utf8": 1,
            "redirects": 1,
            "exintro": True  # Retorna apenas o primeiro parágrafo
        }

        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        if not pages or "-1" in pages:
            return {"erro": "Artigo não encontrado"}

        page = next(iter(pages.values()))
        result = {
            "titulo": page.get("title", topic),
            "extrato": page.get("extract", "Sem conteúdo disponível"),
            "url": f"https://pt.wikipedia.org/wiki/{quote(page.get('title', topic).replace(' ', '_'))}",
            "ultima_edicao": page.get("touched", ""),
            "tamanho": page.get("length", 0),
            "aviso": []
        }

        for cat in page.get("categories", []):
            if "esboço" in cat.get("title", "").lower():
                result["aviso"].append("⚠️ Este artigo é um esboço")

        return result

    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro de conexão: {str(e)}"}
    except Exception as e:
        return {"erro": f"Erro ao processar o artigo: {str(e)}"}
