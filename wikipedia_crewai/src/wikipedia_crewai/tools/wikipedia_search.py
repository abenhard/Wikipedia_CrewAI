import requests
from urllib.parse import quote
from typing import Dict, Any, Union

# Para usar fora da CrewAI e validar tópico
#Busca artigo na Wikipédia em português. Se não encontrado ou ambíguo, retorna sugestões.
def buscar_artigo_wikipedia(topic: str) -> Dict[str, Union[str, list, int]]:

    try:
        topic = topic.strip()
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
            "exintro": True
        }

        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        if not pages or "-1" in pages:
            # Buscar sugestões
            search_params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": topic,
                "utf8": 1
            }

            search_response = requests.get(base_url, params=search_params, timeout=10)
            search_data = search_response.json()
            results = search_data.get("query", {}).get("search", [])

            if results:
                suggestions = [res["title"] for res in results[:5]]
                return {
                    "erro": f"Tópico '{topic}' é ambíguo ou não encontrado.",
                    "sugestoes": suggestions
                }
            else:
                return {"erro": "Artigo não encontrado e nenhuma sugestão foi encontrada."}

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


# 🔧 Tool para CrewAI (usando a função acima)
from crewai.tools import tool

# Ferramenta de pesquisa da Wikipedia
@tool("wikipedia_search")
def wikipedia_search(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool para agentes da CrewAI.
    Espera receber input_data['description'] com o tópico a ser buscado.
    """
    if "input_data" in input_data:
        input_data = input_data["input_data"]

    topic = input_data.get("description", "").strip()
    return buscar_artigo_wikipedia(topic)

