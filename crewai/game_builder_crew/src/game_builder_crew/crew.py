import os
from typing import List

from dotenv import load_dotenv

from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()


@CrewBase
class GameBuilderCrew:
    """GameBuilderCrewai crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # 定义LLM
    llm = LLM(
        model=os.getenv("DEEPSEEK_MODEL"),
        temperature=0,
        base_url=os.getenv("DEEPSEEK_API_BASE"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def senior_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_engineer_agent"],  # type: ignore[index]
            allow_delegation=False,
            llm=self.llm,
            verbose=True,
        )

    @agent
    def qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["qa_engineer_agent"],  # type: ignore[index]
            allow_delegation=False,
            llm=self.llm,
            verbose=True,
        )

    @agent
    def chief_qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["chief_qa_engineer_agent"],  # type: ignore[index]
            allow_delegation=True,
            llm=self.llm,
            verbose=True,
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config["code_task"],  # type: ignore[index]
            agent=self.senior_engineer_agent(),
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_task"],  # type: ignore[index]
            agent=self.qa_engineer_agent(),
        )

    @task
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_task"],  # type: ignore[index]
            agent=self.chief_qa_engineer_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GameBuilderCrewai crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
