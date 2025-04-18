import os
import re
from crewai import Agent, Crew, Process, Task, CrewOutput
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from .models import GeneratedArticle
from .tools.wikipedia_search import wikipedia_search, buscar_artigo_wikipedia  
from .utils.save_article import save_article_to_file

@CrewBase
class WikipediaCrewai():
    """WikipediaCrewai crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.groq_llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL_NAME"),
            temperature=0.6
        )
        os.environ["OPENAI_API_KEY"] = "no-key"
        os.environ["ANTHROPIC_API_KEY"] = "no-key"

    @agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            tasks=[self.write_article_task],
            llm=self.groq_llm,
            tools=[wikipedia_search], 
            verbose=os.getenv("DEBUG"),
            allow_delegation=False
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            llm=self.groq_llm,
            verbose=os.getenv("DEBUG"),
            allow_delegation=False,
            max_rpm=15
        )

    @task
    def write_article_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_article_task'],
            input_keys=["description"],
            output_file='article.md'
        )

    @task
    def content_editor_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_editor_task'],
            output_file='article.md',
            callback=lambda _: print("✅ Edits saved to article.md")
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def clean_output(self, text: str) -> str:
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    def run(self, topic: str) -> GeneratedArticle:
        # Buscar contexto da Wikipedia para o tópico fornecido
        wiki_result = buscar_artigo_wikipedia(topic)

        if "erro" in wiki_result:
            raise ValueError(wiki_result["erro"])

        context = wiki_result.get("extrato", "Conteúdo indisponível")

        inputs = {
            "topic": topic,
            "context": context
        }

        result = self.crew().kickoff(inputs=inputs)

        if isinstance(result, CrewOutput):
            cleaned = self.clean_output(result.raw)
        else:
            cleaned = self.clean_output(result)

        save_article_to_file(topic, cleaned)

        return GeneratedArticle(
            topic=topic,
            content=cleaned,
            word_count=len(cleaned.split()),
            source_url=wiki_result.get("url", ""),
            reliability_flags=wiki_result.get("aviso", [])
        )
