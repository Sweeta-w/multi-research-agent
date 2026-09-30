from crewai import Task, Crew, Process
from agents.researcher import create_researcher_agent
from agents.analyst import create_analyst_agent
from agents.writer import create_writer_agent

def execute_stage(stage_name: str, topic_or_input: str, model_name: str, status_callback=None) -> str:
    """
    Executes specific agent stages while maintaining isolated model contexts and updating UI callbacks.
    """
    researcher = create_researcher_agent(model_name)
    analyst = create_analyst_agent(model_name)
    writer = create_writer_agent(model_name)

    if stage_name == "research":
        if status_callback:
            status_callback("🔍 **Senior Technical Researcher**", "Extracting core facts, mechanisms, and background context...")
        
        task = Task(
            description=f"Conduct deep, exhaustive technical research on: '{topic_or_input}'. Extract verified facts, architectures, and key details.",
            expected_output="Detailed factual research summary.",
            agent=researcher
        )
        crew = Crew(agents=[researcher], tasks=[task], process=Process.sequential)
        return str(crew.kickoff())

    elif stage_name == "analysis":
        if status_callback:
            status_callback("📊 **Data & Strategy Analyst**", "Cross-evaluating research data, filtering noise, and structuring insights...")
        
        task = Task(
            description=f"Analyze these raw research findings:\n\n{topic_or_input}\n\nIdentify strategic patterns, trade-offs, and structure key takeaways.",
            expected_output="Structured analytical takeaways and conceptual breakdown.",
            agent=analyst
        )
        crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential)
        return str(crew.kickoff())

    elif stage_name == "writing":
        if status_callback:
            status_callback("✍️️ **Lead Technical Writer**", "Formatting analyzed insights into a publication-grade Markdown report...")
        
        task = Task(
            description=f"Draft a full, publication-ready research paper in Markdown format based on this analysis:\n\n{topic_or_input}",
            expected_output="A polished Markdown report with executive summaries, clear section headers, and structured bullets.",
            agent=writer
        )
        crew = Crew(agents=[writer], tasks=[task], process=Process.sequential)
        return str(crew.kickoff())