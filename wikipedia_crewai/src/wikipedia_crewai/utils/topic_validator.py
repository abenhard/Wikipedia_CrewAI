from typing import Tuple, Union
from wikipedia_crewai.src.wikipedia_crewai.tools.wikipedia_search import buscar_artigo_wikipedia

def validar_topico(topic: str) -> Tuple[bool, Union[str, list]]:
    """
    Valida um tópico usando a Wikipedia.
    Retorna:
      - (True, artigo) se o tópico for válido e o artigo encontrado.
      - (False, lista de sugestões) se o tópico for ambíguo ou não encontrado.
    """
    resultado = buscar_artigo_wikipedia(topic)

    if "erro" in resultado:
        sugestoes = resultado.get("sugestoes", [])
        return False, sugestoes

    return True, resultado.get("extrato", "Artigo encontrado, mas sem conteúdo.")
