from crewai import Agent
from config.llm_config import get_groq_llm

def create_analyst_agent(model_name: str):
    """
    Creates the Data & Strategy Analyst agent instance.
    """
    return Agent(
        role="Data & Strategy Analyst",
        goal="Filter raw research data, detect strategic patterns, and derive actionable conclusions.",
        backstory="""You are a pragmatic systems analyst. You eliminate redundancies, evaluate trade-offs, 
        and structure factual data into clear, actionable logic blocks.""",
        verbose=True,
        allow_delegation=False,
        llm=get_groq_llm(model_name=model_name)
    )