from crewai import Agent

from crew.llm import get_llm


def create_writer():

    return Agent(
        role="Research Report Writer",

        goal=(
            "Create a clear, professional research report "
            "using the verified evidence."
        ),

        backstory=(
            "You are an experienced research writer. "
            "You turn verified research into a structured "
            "and readable report while clearly distinguishing "
            "evidence, interpretation, and uncertainty."
        ),

        llm=get_llm(),

        verbose=False,

        allow_delegation=False,

        max_iter=6,
    )