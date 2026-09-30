from crewai import Agent
from config.llm_config import get_groq_llm

def create_researcher_agent(model_name: str):
    """
    Creates the Senior Technical Researcher agent instance.
    """
    return Agent(
        role="Senior Technical Researcher",
        goal="Gather exhaustive, factual, and structured information on the target research subject.",
        backstory="""You are a elite technical researcher with a knack for deep synthesis.
        You extract core concepts, historical context, underlying mechanisms, and current industry trends.""",
        verbose=True,
        allow_delegation=False,
        llm=get_groq_llm(model_name=model_name)
    )