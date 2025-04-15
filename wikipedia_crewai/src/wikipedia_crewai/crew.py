import os
from crewai import Agent, Crew, Process, Task
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
        # Initialize with explicit no-LLM fallback
        self.groq_llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL_NAME"),
            temperature=0.6
        )
        self.gemini_llm = ChatGoogleGenerativeAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            model=os.getenv("GEMINI_MODEL_NAME"),
            temperature=0.6
        )

        # Block all OpenAI fallbacks
        os.environ["OPENAI_API_KEY"] = "no-key"
        os.environ["ANTHROPIC_API_KEY"] = "no-key"
    @agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            tasks=[self.write_article_task],
            llm=self.groq_llm,
            tools=[wikipedia_search],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            llm=self.groq_llm,
            verbose=True,
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