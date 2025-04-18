# Criador de artigos usando CrewAI com FastAPI

Este projeto integra um sistema de geração de artigos baseado em [CrewAI](https://github.com/joaomdmoura/crewai) com uma interface web desenvolvida com [FastAPI](https://fastapi.tiangolo.com/). O conteúdo gerado é baseado em dados da Wikipedia, e o artigo final é formatado em Markdown com revisão e estruturação feitas por agentes autônomos.

## 🚀 Funcionalidades

- Busca inteligente de tópicos na Wikipedia
- Sugestão de tópicos em caso de ambiguidade ou não encontrado
- Geração de artigos com no mínimo **300 palavras**
- Validação e edição automatizadas por agentes
- Interface web estilo ChatGPT
- Suporte a Markdown com destaques visuais de confiabilidade

## 📂 Estrutura do Projeto

```
Wikipedia_CrewAI-FAST_API/
├── api.py                       # Inicialização da API FastAPI
├── requirements.txt             # Dependências do projeto
├── static/style.css             # Estilo da interface web
├── templates/chat.html          # Template HTML com suporte a Markdown
├── .env                         # Variáveis de ambiente (.gitignore recomendado)
├── wikipedia_crewai/            # Código principal do sistema multiagente
│   ├── article.md               # Artigo gerado de exemplo
│   ├── report.md                # Relatório de qualidade
│   ├── pyproject.toml           # Configuração de build
│   ├── knowledge/               # Preferências do usuário
│   └── src/wikipedia_crewai/   # Módulo principal com CrewAI
└── .idea/                       # Configurações do ambiente (PyCharm)
```

## ⚙️ Requisitos

- Python >=3.10 <3.13 
- Variáveis definidas no `.env`
- Dependências listadas no `requirements.txt`

## 🧠 Como funciona

O sistema usa a biblioteca CrewAI para organizar múltiplos agentes autônomos responsáveis por:

1. **Pesquisar** conteúdo da Wikipedia.
2. **Validar** a confiabilidade e completude.
3. **Escrever** um artigo estruturado.
4. **Editar** com foco em clareza, coesão e estilo.
5. **Publicar** o resultado na interface web.

## ▶️ Primeiros passos para rodar o projeto

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
     ```bash
     python -m venv venv
     .venv\Scripts\activate 
     ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure .env e crew.py na próxima seção. 

## 🧠 Configuração do Modelo de Linguagem (LLM)

O sistema utiliza um LLM (Large Language Model) fornecido por serviços como **Groq**, **OpenAI**, **Anthropic**, entre outros. A escolha do provedor e do modelo é feita via variável de ambiente no arquivo `.env` e configurações no aquivo crew.py.
Por padrão CrewAI utiliza o OPENAI.

## ⚙️ Configuração do `.env`e como definir o provedor e modelo

Antes de executar o sistema, é necessário configurar o arquivo `.env` na raiz do projeto, por exemplo usando um modelo GROQ:

GROQ_MODEL_NAME=groq/llama3-8b-8192
- A parte **antes da barra** (`groq/`) indica o **provedor**.
- A parte **depois da barra** (`llama3-8b-8192`) indica o **modelo**.

Além disso, é necessário informar a chave da API correspondente, por exemplo:

GROQ_API_KEY=sua-chave-groq-aqui

A variável `DEBUG` controla se os agentes devem funcionar no modo **verbose**, útil para depuração.
DEBUG=false

### 📌 Provedores suportados (exemplos)

| Provedor   | Exemplo de modelo                      | Observação                               |
|------------|----------------------------------------|------------------------------------------|
| `groq`     | `groq/llama3-8b-8192`                  | Modelos hospedados pela Groq             |
| `openai`   | `openai/gpt-4`                         | Requer `OPENAI_API_KEY`                  |
| `anthropic`| `anthropic/claude-3-opus-20240229`     | Requer `ANTHROPIC_API_KEY`               |

---

## 🛠️ Alterando o LLM no código (`crew.py`)
> 💡 Se desejar usar um provedor que seja GROQ(como OpenAI ou Anthropic), você pode adaptar o arquivo `crew.py`, que atualmente inicializa o `ChatGroq` da seguinte forma dentro de init:

```python
self.groq_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL_NAME"),
    temperature=0.6
)

# Evita conflito com outros provedores, CASO FOR USAR OPENAI COMENTE A SEGUINTES LINHAS
os.environ["OPENAI_API_KEY"] = "no-key"
os.environ["ANTHROPIC_API_KEY"] = "no-key"
```

Para usar OpenAI ou Anthropic, altere a inicialização do LLM conforme a classe desejada , `ChatAnthropic`, por exemplo:
```python
self.antho_llm = ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model=os.getenv("ANTHROPIC_MODEL_NAME"),
        temperature=0.6
    )
```
Na parte dos agentes, modifique a variavel 'llm' em ambos:
```python
@agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            tasks=[self.write_article_task],
            llm=self.groq_llm, #AQUI MUDE PARA self.antho_llm se deseja usar o modelo ANTHROPIC ou deixa assim se deseja que um agente use GROQ e outro o Anthopic, por exemplo.
            tools=[wikipedia_search], 
            verbose=os.getenv("DEBUG"),
            allow_delegation=False
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            llm=self.antho_llm , # AQUI FOI MODIFICADO POR EXEMPLO
            verbose=os.getenv("DEBUG"),
            allow_delegation=False,
            max_rpm=15
        )
```

## ▶️ Passos finais para rodar o projeto

5. Execute a API (substitua a porta se desejar) no terminal, Observação tenha certeza de estar na raiz do projeto 'Wikipedia_CrewAI-FAST_API/':
   ```bash
   python -m uvicorn api:app --reload --port 8001
   ```

6. Acesse no navegador ou pelo ip no terminal:
   ```
   http://localhost:8001
   ```

## ✍️ Exemplo de uso

Digite um tópico como **"inteligência artificial"** ou **"Brasil"**, e o sistema irá:

- Buscar conteúdo relevante da Wikipedia
- Verificar ambiguidade e sugerir variações se necessário
- Gerar um artigo em Markdown com 300+ palavras
- Aplicar destaques visuais de confiabilidade
- Exibir o conteúdo na interface web
- Salvar o artigo automaticamente na pasta `artigos/`

> 📝 Os arquivos são salvos com o nome do tópico + data. Se já existir, será salvo com sufixos `_v1`, `_v2`, etc.
> - Exemplo: `carros_20-02-2026.md` → `carros_20-02-2026_v1.md`

## 📄 Licença

Este projeto é licenciado sob os termos da [MIT License](LICENSE).

---

Contribuições são bem-vindas! Abra uma issue ou pull request. 🚀
