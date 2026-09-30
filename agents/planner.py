from crewai import Agent

from crew.llm import get_llm


def create_planner():

    return Agent(
        role="Research Planner",

        goal=(
            "Understand the user's research question and create "
            "a focused research plan."
        ),

        backstory=(
            "You are an experienced research planner. "
            "You break broad questions into smaller research areas "
            "and identify the information needed to answer them."
        ),

        llm=get_llm(),

        verbose=False,

        allow_delegation=False,

        max_iter=5,
    )