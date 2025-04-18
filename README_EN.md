# 🧠 Article Generator with CrewAI + FastAPI

This project integrates an article generation system based on [CrewAI](https://github.com/joaomdmoura/crewai) with a web interface built using [FastAPI](https://fastapi.tiangolo.com/). The generated content is sourced from Wikipedia, formatted in Markdown, and reviewed by autonomous agents.

---

## 🚀 Features

- Smart topic search on Wikipedia  
- Alternative suggestions in case of ambiguity or missing articles  
- Generates articles with at least **300 words**  
- Automatic validation and editing by agents  
- WhatsApp-style web interface  
- Markdown support with visual trust indicators  

---

## 📁 Project Structure

```
Wikipedia_CrewAI-FAST_API/
├── api.py                       # FastAPI initialization
├── requirements.txt             # Project dependencies
├── static/style.css             # Web interface styling
├── templates/chat.html          # HTML template with Markdown support
├── .env                         # Environment variables (.gitignore recommended)
├── wikipedia_crewai/            # Main multi-agent system code
│   ├── article.md               # Example generated article
│   ├── report.md                # Quality report
│   ├── pyproject.toml           # Build configuration
│   ├── knowledge/               # User preferences
│   └── src/wikipedia_crewai/   # Core CrewAI module
└── .idea/                       # IDE configs (optional)
```

---

## ⚙️ Requirements

- Python 3.10 to 3.12  
- Properly configured `.env` file  
- Dependencies listed in `requirements.txt`

---

## 🧠 How It Works

The user enters a topic on the site. This topic is validated using the `topic_validator` tool.  
If the article is ambiguous or not found on Wikipedia, suggestions are shown.

Once validated, two CrewAI agents are triggered:

1. **`article_writer`**: Writes a structured article based on Wikipedia content retrieved via the `wikipedia_search` tool.
2. **`content_editor`**: Enhances the article's clarity, coherence, and style.

The final article is displayed to the user and saved in the `artigos/` folder.

---

## ▶️ Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/abenhard/Wikipedia_CrewAI.git
   cd Wikipedia_CrewAI
   ```

2. Create and activate a virtual environment:

   - **Linux/macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

   - **Windows:**
     ```powershell
     python -m venv venv
     .env\Scripts\Activate.ps1
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file and `crew.py` as shown below.

---

## 🧩 LLM Configuration

The LLM provider and model (Groq, OpenAI, Anthropic etc.) are configured via the `.env` file and `crew.py`.

Example `.env` with Groq:
```env
GROQ_MODEL_NAME=groq/llama3-8b-8192
GROQ_API_KEY=your-api-key
DEBUG=false
```

| Provider    | Example Model                        | Note                         |
|-------------|--------------------------------------|------------------------------|
| `groq`      | `groq/llama3-8b-8192`                | Requires `GROQ_API_KEY`      |
| `openai`    | `openai/gpt-4`                       | Requires `OPENAI_API_KEY`    |
| `anthropic` | `anthropic/claude-3-opus-20240229`   | Requires `ANTHROPIC_API_KEY` |

---

## ⚙️ Editing the LLM in `crew.py`

Example using `ChatGroq`:

```python
self.groq_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL_NAME"),
    temperature=0.6
)
```

To use OpenAI or Anthropic, replace with:

```python
self.antho_llm = ChatAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=os.getenv("ANTHROPIC_MODEL_NAME"),
    temperature=0.6
)
```

Then update the agent LLMs:

```python
llm=self.antho_llm  # Or self.groq_llm, as desired
```

---

## ▶️ Running the App

5. Run the FastAPI server (change the port if needed):
   ```bash
   python -m uvicorn api:app --reload --port 8001
   ```

6. Open your browser and go to:
   ```
   http://localhost:8001
   ```

---

## ✍️ Example Usage

Enter a topic such as **"artificial intelligence"** or **"Brazil"**. The system will:

- Fetch Wikipedia content  
- Handle ambiguities and offer suggestions  
- Generate a Markdown article with 300+ words  
- Add visual reliability indicators  
- Display it in the web interface  
- Save it in `artigos/` automatically

> Files are saved using topic + date. Multiple versions get suffixes like `_v1`, `_v2`, etc.  
> Example: `cars_20-02-2026.md` → `cars_20-02-2026_v1.md`

---

## 🐞 Known Issues

- LLM internal reasoning may leak into the article even with `DEBUG=false`  
- Article quality depends on the LLM model used  

---

## 📄 License

Distributed under the [MIT License](LICENSE).

---

Contributions are welcome!  
Feel free to open an issue or pull request. 🚀