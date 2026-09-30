from crewai import Agent

from crew.llm import get_llm
from tools.web_search import WebSearchTool


def create_researcher():

    search_tool = WebSearchTool()

    return Agent(
        role="Web Research Specialist",

        goal=(
            "Find reliable evidence and relevant sources "
            "that answer the research question."
        ),

        backstory=(
            "You are a careful web research specialist. "
            "You search for official sources, academic material, "
            "government information, research organizations, "
            "reputable reports, and recent evidence."
        ),

        tools=[search_tool],

        llm=get_llm(),

        verbose=False,

        allow_delegation=False,

        max_iter=8,
    )