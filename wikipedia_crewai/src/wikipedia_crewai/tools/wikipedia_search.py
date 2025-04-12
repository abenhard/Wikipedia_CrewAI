from crewai.tools import tool
import requests
from urllib.parse import quote
import json
from typing import Union, Dict, Any


@tool("wikipedia_search")
def wikipedia_search(input_data: Union[str, Dict[str, Any]]) -> dict:
    """Ferramenta de análise forense para Wikipedia em português (pt.wikipedia.org)

    Args:
        input_data: Either a string with the article title or a dictionary with article info

    Returns:
        Dicionário estruturado para validação de artigos
    """
    # Debug print to see raw input
    print(f"\nDEBUG - Raw input received: {input_data} (type: {type(input_data)})\n")

    # Initialize topic variable
    topic = ""

    # Handle string input (could be JSON string)
    if isinstance(input_data, str):
        try:
            # Try to parse as JSON
            parsed = json.loads(input_data)
            if isinstance(parsed, dict):
                input_data = parsed
            else:
                topic = str(parsed)
        except json.JSONDecodeError:
            # If not JSON, use as direct topic
            topic = input_data.strip()

    # Handle dictionary input
    if isinstance(input_data, dict):
        # Check for direct topic key
        if "topic" in input_data:
            topic = str(input_data["topic"])
        # Check for nested structure the agent is using
        elif "input_data" in input_data:
            nested = input_data["input_data"]
            if isinstance(nested, dict):
                topic = nested.get("description") or nested.get("value") or ""
            else:
                topic = str(nested)
        # Handle case where dictionary is the topic itself
        elif "description" in input_data:
            topic = input_data["description"]

    # Final fallback if we still don't have a topic
    if not topic:
        if isinstance(input_data, dict):
            # Try to get first string value from dict
            for value in input_data.values():
                if isinstance(value, str):
                    topic = value
                    break
        else:
            topic = str(input_data)

    # Clean and validate topic
    topic = topic.strip() if isinstance(topic, str) else ""
    if not topic:
        return {"erro": "Nenhum tópico válido fornecido para pesquisa"}

    print(f"DEBUG - Using topic: {topic}")

    # Rest of your Wikipedia API implementation...
    base_url = "https://pt.wikipedia.org/w/api.php"
    encoded_topic = quote(topic.replace(' ', '_'))

    params_content = {
        "action": "query",
        "format": "json",
        "prop": "extracts|info|revisions|categories|flagged",
        "titles": topic,
        "inprop": "protection",
        "rvprop": "timestamp|user|comment|size",
        "rvlimit": 5,
        "rvdir": "newer",
        "explaintext": True,
        "utf8": 1,
        "redirects": 1,
        "exsectionformat": "plain"
    }

    try:
        content_response = requests.get(base_url, params=params_content, timeout=10).json()
        pages = content_response.get("query", {}).get("pages", {})

        if not pages or "-1" in pages:
            return {"erro": f"Artigo '{topic}' não encontrado na Wikipedia em português"}

        page = next(iter(pages.values()))

        if "missing" in page:
            return {"erro": f"O artigo '{topic}' não existe na Wikipedia em português"}

        nivel_protecao = "desprotegido"
        if "protection" in page and len(page["protection"]) > 0:
            nivel_protecao = page["protection"][0].get("level", "desprotegido")

        edicoes = page.get("revisions", [])[:5]
        ultima_edicao = edicoes[-1]["timestamp"] if edicoes else "N/A"

        extracto = page.get("extract", "")
        if not extracto:
            return {"erro": f"O artigo '{topic}' existe mas não tem conteúdo extraível"}

        citacoes_necessarias = extracto.lower().count("carece de fontes") + extracto.lower().count("precisa de citação")
        eh_esboco = any("esboço" in cat.get("title", "").lower() for cat in page.get("categories", []))
        eh_destacado = page.get("flagged", {}).get("is_featured", False)

        reversoes = sum(1 for ed in edicoes if
                        "revert" in ed.get("comment", "").lower() or "reversão" in ed.get("comment", "").lower())
        risco_edicoes = "Alto" if reversoes >= 3 else "Moderado" if reversoes >= 1 else "Baixo"

        pontuacao = (
            5 if eh_destacado else
            4 if not eh_esboco and nivel_protecao == "autoconfirmed" else
            3 if citacoes_necessarias < 3 else
            2 if risco_edicoes == "Alto" or citacoes_necessarias >= 5 else
            1
        )

        return (
            "## Wikipedia Quality Report: {topic}\n"
            "### Basic Metadata\n"
            f"- URL: {result['url']}\n"
            f"- Length: {result['chars']} characters\n"
            f"- Last edit: {result['date']}\n\n"
            "### Reliability Indicators\n"
            f"- Protection Level: {result['protection_level']}\n"
            f"- Edit Risk: {result['edit_risk']}\n"
            f"- Citations Needed: {result['citations_needed']}\n"
            f"- Stub: {result['is_stub']}\n"
            f"- Featured: {result['is_featured']}\n\n"
            "### Final Assessment\n"
            f"Reliability Score: {result['reliability_score']}/5\n\n"
            f"Content Preview: {result['content']}"
        )

    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro de conexão: {str(e)}"}
    except Exception as e:
        return {"erro": f"Erro ao analisar o artigo: {str(e)}"}