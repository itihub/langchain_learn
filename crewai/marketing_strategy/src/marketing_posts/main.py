#!/usr/bin/env python
import sys

from marketing_posts.crew import MarketingPostsCrew


def run():
    # 替换为您的输入，它将自动插入任何任务和代理信息
    inputs = {
        "customer_domain": "crewai.com",
        "project_description": """
CrewAI，作为多智能体系统的领先提供商，旨在为其企业客户革新营销自动化。该项目涉及开发创新营销策略，以展示CrewAI的先进AI驱动解决方案，强调易用性、可扩展性和集成能力。该营销活动将针对中大型企业中具有技术敏感度的决策者，突出成功案例和CrewAI平台的变革潜力。

客户领域:AI和自动化解决方案
项目概述:创建全面的营销活动，提高企业客户对CrewAI服务的认知和采用。
""",
    }
    MarketingPostsCrew().crew().kickoff(inputs=inputs)


def train():
    """
    为指定的迭代次数训练团队
    """
    inputs = {
        "customer_domain": "crewai.com",
        "project_description": """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize marketing automation for its enterprise clients. This project involves developing an innovative marketing strategy to showcase CrewAI's advanced AI-driven solutions, emphasizing ease of use, scalability, and integration capabilities. The campaign will target tech-savvy decision-makers in medium to large enterprises, highlighting success stories and the transformative potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost awareness and adoption of CrewAI's services among enterprise clients.
""",
    }
    try:
        MarketingPostsCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
