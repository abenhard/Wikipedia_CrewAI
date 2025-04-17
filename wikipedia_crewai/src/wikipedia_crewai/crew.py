import os
import re
from crewai import Agent, Crew, Process, Task, CrewOutput
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool
from .tools.wikipedia_search import wikipedia_search

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
            input_keys=["topic"],
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

    def run(self, topic: str) -> str:
        result = self.crew().kickoff(inputs={"topic": topic})

        # Verifique se result é do tipo CrewOutput
        if isinstance(result, CrewOutput):
            # Exibir a estrutura do objeto para entender melhor
            print(result.__dict__)  # Isso vai mostrar os atributos do objeto
            # Tentando acessar o campo "raw" ou equivalente
            cleaned = self.clean_output(result.raw)  # A chave pode ser 'raw' ou algo semelhante
        else:
            # Caso o resultado não seja um CrewOutput, use o fluxo anterior
            cleaned = self.clean_output(result)

        with open("article.md", "w", encoding="utf-8") as f:
            f.write(cleaned)

        return cleaned



