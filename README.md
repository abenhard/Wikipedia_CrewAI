# Criador de artigos usando CrewAI com FastAPI

Este projeto integra um sistema de geração de artigos baseado em [CrewAI](https://github.com/joaomdmoura/crewai) com uma interface web em [FastAPI](https://fastapi.tiangolo.com/). O sistema utiliza conteúdo da Wikipedia como base e transforma as informações em artigos formatados em Markdown com revisão e estruturação por agentes autônomos.

## 🚀 Funcionalidades

- Busca inteligente de tópicos na Wikipedia
- Geração de artigos com mínimo de 300 palavras
- Validação e edição automatizada por agentes
- Interface web com visual estilo de Chat
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

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:

   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```

   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Adicione sua API key e modelo no .env
   ```
   Na raiz no projeto modifique o arquivo .env 
   ```
6. Execute a API( substituindo 8001 pela porta que desejar):
   ```bash
   python -m uvicorn api:app --reload --port 8001
   ```

7. Acesse via navegador( substituindo 8001 pela porta usando no passo 5):
   ```
   http://localhost:8001
   ```

## ✍️ Exemplo de uso

Digite um tópico como **"inteligência artificial"** ou **"Brasil"**, e o sistema irá:
- Buscar o conteúdo relevante da Wikipedia
- Verificar ambiguidade
- Gerar um artigo completo em Markdown
- Exibir o resultado na interface com destaques visuais
- Salvar o artigo em uma pasta 'artigos' na raiz do projeto no formato md.

- Obs: o artigo criado é nomeado com  o tópico digitado + data da criação, se caso um arquivo de mesmo nome ja exista na pasta, ele é então adicionado v1, v2, assim sucessivamente . 
- Exemplo: carros_20-02-2026 e  carros_20-02-2026_v1

## 📄 Licença

Este projeto é licenciado sob os termos da [MIT License](LICENSE).

---

Contribuições são bem-vindas! 🚀
