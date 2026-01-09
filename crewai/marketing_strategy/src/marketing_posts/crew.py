import os
from typing import List

# Uncomment the following line to use an example of a custom tool
# from marketing_posts.tools.custom_tool import MyCustomTool
# Check our tools documentations for more information on how to use them
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

load_dotenv()


class MarketStrategy(BaseModel):
    """市场策略模型"""

    name: str = Field(..., description="市场策略的名称")
    tatics: List[str] = Field(..., description="市场策略中使用的战术列表")
    channels: List[str] = Field(..., description="市场策略中使用的渠道列表")
    KPIs: List[str] = Field(..., description="市场策略中使用的关键绩效指标列表")


class CampaignIdea(BaseModel):
    """营销活动创意模型"""

    name: str = Field(..., description="营销活动创意的名称")
    description: str = Field(..., description="营销活动创意的描述")
    audience: str = Field(..., description="营销活动创意的目标受众")
    channel: str = Field(..., description="营销活动创意的渠道")


class Copy(BaseModel):
    """文案模型"""

    title: str = Field(..., description="文案的标题，中文输出")
    body: str = Field(..., description="文案的正文，中文输出")


@CrewBase
class MarketingPostsCrew:
    """营销帖子团队"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    # 定义LLM
    llm = LLM(
        model=os.getenv("DEEPSEEK_MODEL"),
        temperature=0,
        base_url=os.getenv("DEEPSEEK_API_BASE"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )

    @agent
    def lead_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["lead_market_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            llm=self.llm,
            memory=False,
        )

    @agent
    def chief_marketing_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["chief_marketing_strategist"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            llm=self.llm,
            memory=False,
        )

    @agent
    def creative_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["creative_content_creator"],
            verbose=True,
            llm=self.llm,
            memory=False,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"], agent=self.lead_market_analyst()
        )

    @task
    def project_understanding_task(self) -> Task:
        return Task(
            config=self.tasks_config["project_understanding_task"],
            agent=self.chief_marketing_strategist(),
        )

    @task
    def marketing_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["marketing_strategy_task"],
            agent=self.chief_marketing_strategist(),
            output_json=MarketStrategy,
        )

    @task
    def campaign_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config["campaign_idea_task"],
            agent=self.creative_content_creator(),
            output_json=CampaignIdea,
        )

    @task
    def copy_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["copy_creation_task"],
            agent=self.creative_content_creator(),
            context=[self.marketing_strategy_task(), self.campaign_idea_task()],
            output_json=Copy,
        )

    @crew
    def crew(self) -> Crew:
        """创建营销团队"""
        return Crew(
            agents=self.agents,  # 由@agent装饰器自动创建
            tasks=self.tasks,  # 由@task装饰器自动创建
            manager_llm=self.llm,  # 使用层级模式需要添加manager_llm或manager_agent
            process=Process.hierarchical,  # 支持顺序模式和层级模式，如果你想使用层次结构流程 https://docs.crewai.com/how-to/Hierarchical/
            verbose=True,
        )
