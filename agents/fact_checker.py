from crewai import Agent

from crew.llm import get_llm


def create_fact_checker():

    return Agent(
        role="Research Fact Checker",

        goal=(
            "Review the collected research and identify "
            "supported claims, weak evidence, contradictions, "
            "and important limitations."
        ),

        backstory=(
            "You are a rigorous evidence analyst. "
            "You do not automatically trust every claim. "
            "You distinguish facts from interpretations, "
            "identify unsupported statements, and look for "
            "conflicting or outdated evidence."
        ),

        llm=get_llm(),

        verbose=False,

        allow_delegation=False,

        max_iter=6,
    )