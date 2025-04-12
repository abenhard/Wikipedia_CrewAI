import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from .tools.wikipedia_search import wikipedia_search

@CrewBase
class WikipediaCrewai():
    """WikipediaCrewai crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @property
    def llm(self):
        return ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="groq/llama3-8b-8192",
            temperature=0.6
        )

    @agent
    def wikipedia_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['wikipedia_validator'],
            tasks=[self.validate_wikipedia_task],
            llm=None,  # Remove LLM dependency
            tools=[wikipedia_search],
            verbose=True,
            max_iter=1,  # Only needs one tool call
            allow_delegation=False,
            tool_usage_instructions=(
                "STRICT INSTRUCTIONS:\n"
                "1. Call wikipedia_search exactly once with format:\n"
                "Action: wikipedia_search\n"
                "Action Input: {\"topic\": \"ARTICLE_TITLE\"}\n"
                "2. Return the raw tool output without modification"
            )
        )

    @agent
    def article_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_writer'],
            tasks=[self.write_article_task],
            llm=self.llm,
            verbose=True
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'],
            tasks=[self.edit_article_task],
            llm=self.llm,
            verbose=True
        )

    @agent
    def quality_controller(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_controller'],
            tasks=[self.quality_control_task],
            llm=self.llm,
            verbose=True
        )

    @task
    def validate_wikipedia_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_wikipedia_task'],
            output_parser=lambda output: (
                output if isinstance(output, str) and all(
                    section in output for section in [
                        "## Wikipedia Quality Report",
                        "### Basic Metadata",
                        "### Reliability Indicators",
                        "### Final Assessment"
                    ]
                )
                else f"Error: Invalid report format. Got: {output[:200] + '...' if len(str(output)) > 200 else output}"
            ),
            output_file='wikipedia_report.md',
            expected_output="Complete Wikipedia quality report in markdown format with all required sections"
        )

    @task
    def write_article_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_article_task'],
            output_file='report.md'
        )

    @task
    def edit_article_task(self) -> Task:
        return Task(
            config=self.tasks_config['edit_article_task'],
            output_file='report.md'
        )

    @task
    def quality_control_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_control_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
