from crewai import Agent
from config.llm_config import get_groq_llm

def create_writer_agent(model_name: str):
    """
    Creates the Lead Technical Writer agent instance.
    """
    return Agent(
        role="Lead Technical Writer",
        goal="Transform analyzed insights into a publication-grade, beautifully formatted report.",
        backstory="""You are an expert technical author. You craft clear, persuasive, and structured reports
        featuring executive summaries, organized sections, and impactful bullet points.""",
        verbose=True,
        allow_delegation=False,
        llm=get_groq_llm(model_name=model_name)
    )