# Wikipedia CrewAI com FastAPI

Este projeto integra um sistema de geração de artigos baseado em [CrewAI](https://github.com/joaomdmoura/crewai) com uma interface web em [FastAPI](https://fastapi.tiangolo.com/). O sistema utiliza conteúdo da Wikipedia como base e transforma as informações em artigos formatados em Markdown com revisão e estruturação por agentes autônomos.

## 🚀 Funcionalidades

- Busca inteligente de tópicos na Wikipedia
- Resolução de ambiguidade e sugestões quando o tópico não é encontrado
- Geração de artigos com mínimo de 300 palavras
- Validação e edição automatizada por agentes
- Interface web com visual estilo ChatGPT
- Suporte a Markdown com marcações visuais de confiabilidade

## 📂 Estrutura do Projeto

```
Wikipedia_CrewAI-FAST_API/
├── api.py                       # Inicialização da API FastAPI
├── requirements.txt             # Dependências do projeto
├── static/style.css             # Estilo da interface web
├── templates/chat.html          # Template HTML com suporte a Markdown
├── wikipedia_crewai/            # Código principal do sistema multiagente
│   ├── article.md               # Artigo gerado de exemplo
│   ├── report.md                # Relatório de qualidade
│   ├── pyproject.toml           # Configuração de build
│   ├── knowledge/               # Preferências do usuário
│   └── src/wikipedia_crewai/   # Módulo principal com CrewAI
└── .idea/                       # Configurações do ambiente (PyCharm)
```

## ⚙️ Requisitos

- Python 3.10+
- Dependências listadas em `requirements.txt`

## 🧠 Como funciona

O sistema define múltiplos agentes para:
1. **Pesquisar** o conteúdo da Wikipedia.
2. **Validar** a confiabilidade do artigo.
3. **Escrever** o artigo com base no conteúdo coletado.
4. **Editar** o texto para coesão, clareza e estilo.
5. **Publicar** o conteúdo final na interface web.

Os fluxos são organizados com a biblioteca CrewAI, permitindo controle refinado da comunicação entre os agentes.

## ▶️ Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Wikipedia_CrewAI-FAST_API.git
   cd Wikipedia_CrewAI-FAST_API
   ```

2. Instale os pacotes:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a API:
   ```bash
   uvicorn api:app --reload
   ```

4. Acesse via navegador:
   ```
   http://localhost:8000
   ```

## ✍️ Exemplo de uso

Digite um tópico como **"inteligência artificial"** ou **"Brasil"**, e o sistema irá:
- Buscar o conteúdo relevante da Wikipedia
- Verificar ambiguidade
- Gerar um artigo completo em Markdown
- Exibir o resultado na interface com destaques visuais

## 📄 Licença

Este projeto é licenciado sob os termos da [MIT License](LICENSE).

---

Contribuições são bem-vindas! 🚀
