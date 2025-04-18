# 🧠 Criador de Artigos com CrewAI + FastAPI

Este projeto integra um sistema de geração de artigos baseado em [CrewAI](https://github.com/joaomdmoura/crewai) com uma interface web desenvolvida em [FastAPI](https://fastapi.tiangolo.com/). O conteúdo é extraído da Wikipedia, estruturado em Markdown e revisado por agentes autônomos.

---

## 🚀 Funcionalidades

- Busca inteligente de tópicos na Wikipedia  
- Sugestão de alternativas em caso de ambiguidade ou ausência de artigos  
- Geração de artigos com no mínimo **300 palavras**  
- Validação e edição automática por agentes  
- Interface web no estilo WhatsApp  
- Suporte a Markdown com destaques visuais de confiabilidade  

---

## 📁 Estrutura do Projeto

```
Wikipedia_CrewAI-FAST_API/
├── api.py                       # Inicialização da API FastAPI
├── requirements.txt             # Dependências do projeto
├── static/style.css             # Estilo da interface web
├── templates/chat.html          # Template HTML com suporte a Markdown
├── .env                         # Variáveis de ambiente (.gitignore recomendado)
├── wikipedia_crewai/            # Código principal do sistema multiagente
│   ├── article.md               # Exemplo de artigo gerado
│   ├── report.md                # Relatório de qualidade
│   ├── pyproject.toml           # Configuração de build
│   ├── knowledge/               # Preferências do usuário
│   └── src/wikipedia_crewai/   # Módulo principal com CrewAI
└── .idea/                       # Configurações do PyCharm (opcional)
```

---

## ⚙️ Requisitos

- Python 3.10 até 3.12  
- Arquivo `.env` configurado corretamente  
- Dependências listadas em `requirements.txt`

---

## 🧠 Como Funciona

O usuário informa um tópico no site. Esse tópico é validado pela ferramenta `topic_validator`.  
Se o artigo da Wikipedia não for encontrado ou for ambíguo, sugestões alternativas são apresentadas.

Uma vez validado, dois agentes da CrewAI são ativados:

1. **`article_writer`**: escreve um artigo estruturado baseado em informações obtidas pela ferramenta `wikipedia_search`, que acessa a API da Wikipedia.
2. **`content_editor`**: edita o artigo gerado, melhorando clareza, fluidez e estilo.

O artigo final é exibido ao usuário e salvo na pasta `artigos/`.

---

## ▶️ Primeiros Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/abenhard/Wikipedia_CrewAI.git
   cd Wikipedia_CrewAI
   ```

2. Crie e ative um ambiente virtual:

   - **Linux/macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o `.env` e o arquivo `crew.py` conforme instruções abaixo.

---

## 🧩 Configuração do Modelo de Linguagem (LLM)

A escolha do provedor e do modelo LLM (Groq, OpenAI, Anthropic etc.) é feita via `.env` e `crew.py`.

Use o template .env incluido ou use este exemplo de `.env` para uso com Groq:
```env
GROQ_MODEL_NAME=groq/llama3-8b-8192
GROQ_API_KEY=sua-chave-aqui
DEBUG=false
```

| Provedor   | Exemplo de modelo                      | Observação                    |
|------------|----------------------------------------|-------------------------------|
| `groq`     | `groq/llama3-8b-8192`                  | Requer `GROQ_API_KEY`         |
| `openai`   | `openai/gpt-4`                         | Requer `OPENAI_API_KEY`       |
| `anthropic`| `anthropic/claude-3-opus-20240229`     | Requer `ANTHROPIC_API_KEY`    |

---

## ⚙️ Alterando o LLM em `crew.py`

Exemplo de configuração com `ChatGroq`:

```python
self.groq_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL_NAME"),
    temperature=0.6
)
```

Para usar Anthropic por exemplo, crie:

```python
self.antho_llm = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=os.getenv("ANTHROPIC_MODEL_NAME"),
    temperature=0.6
)
```
Caso for usar OPENAI comentar ou excluir as linhas abaixo, que são usadas para evitar conflitos com outras LLM's posi CrewAI usa OpenAI por default:
```python
 os.environ["OPENAI_API_KEY"] = "no-key"
 os.environ["ANTHROPIC_API_KEY"] = "no-key"
)
```

E então ajuste nos agentes o campo llm, por exemplo no article_writer:

```python
 @agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            tasks=[self.write_article_task],
            llm=self.groq_llm, # mude aqui para o modelo que deseja usar
            tools=[wikipedia_search], 
            verbose=os.getenv("DEBUG"),
            allow_delegation=False
        )
```

---

## ▶️ Rodando a Aplicação

5. Execute a API (substitua a porta, se necessário):
   ```bash
   python -m uvicorn api:app --reload --port 8001
   ```

6. Acesse pelo navegador:
   ```
   http://localhost:8001
   ```

---

## ✍️ Exemplo de Uso

Digite um tópico como **"inteligência artificial"** ou **"Brasil"**. O sistema irá:

- Buscar o artigo na Wikipedia  
- Verificar ambiguidade e sugerir variações  
- Gerar um artigo em Markdown com 300+ palavras  
- Marcar trechos com alertas visuais sobre confiabilidade  
- Exibir na interface e salvar automaticamente em `artigos/`

> Arquivos são salvos com nome do tópico + data. Versões adicionais ganham sufixos: `_v1`, `_v2`, etc.  
> Ex: `carros_20-02-2026.md` → `carros_20-02-2026_v1.md`

---

## 🐞 Observações 

- Fragmentos do *raciocínio interno* dos modelos podem aparecer no texto, mesmo com `DEBUG=false`  
- A qualidade do artigo depende diretamente do modelo LLM utilizado
- na pasta Wikipedia_CrewAI\wikipedia_crewai\src\wikipedia_crewai esta um arquivo main.py que pode ser utilizado para testar o crewai sem usar o frontend, porém NÃO há validação do tópico:
  
```bash
   cd Wikipedia_CrewAI/wikipedia_crewai/src/wikipedia_crewai
   crewai run
 ```
- Você pode alterar o tópico testado alternando:
```python
   def run():
    inputs = {
        'topic': 'Placas de video', #Altere aqui o tópico a ser utilizado
        'current_year': str(datetime.now().year)
    }
 ```
---

## 📄 Licença

Distribuído sob a licença [MIT](LICENSE).

---

Contribuições são muito bem-vindas!  
Abra uma issue ou envie um pull request. 🚀
