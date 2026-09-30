from crewai import Crew, Process, Task

from agents.planner import create_planner
from agents.researcher import create_researcher
from agents.fact_checker import create_fact_checker
from agents.writer import create_writer


AGENT_ORDER = [
    {
        "name": "Research Planner",
        "icon": "🧭",
        "description": "Breaking the research question into focused areas.",
    },
    {
        "name": "Web Researcher",
        "icon": "🔎",
        "description": "Searching the web and collecting evidence.",
    },
    {
        "name": "Fact Checker",
        "icon": "🛡️",
        "description": "Checking claims, evidence, and contradictions.",
    },
    {
        "name": "Research Writer",
        "icon": "✍️",
        "description": "Writing the final research report.",
    },
]


def build_crew(status_callback=None):

    planner = create_planner()

    researcher = create_researcher()

    fact_checker = create_fact_checker()

    writer = create_writer()

    # -----------------------------------
    # TASK 1 — Planning
    # -----------------------------------

    planning_task = Task(
        description="""
        Analyze this research question:

        {topic}

        Create a focused research plan.

        Identify:

        1. The main research question.
        2. Important subtopics.
        3. Specific questions that need answers.
        4. Useful search keywords.
        5. Types of evidence that should be collected.

        Do not write the final report.
        """,

        expected_output="""
        A concise research plan containing:

        - Main question
        - Research areas
        - Research questions
        - Search keywords
        - Evidence requirements
        """,

        agent=planner,
    )

    # -----------------------------------
    # TASK 2 — Research
    # -----------------------------------

    research_task = Task(
        description="""
        Conduct web research using the research plan.

        Research topic:

        {topic}

        Search for reliable evidence.

        Prioritize:

        - Official organizations
        - Government sources
        - Academic sources
        - Research institutions
        - Reputable reports
        - Recent information

        For important findings, record:

        - Claim
        - Evidence
        - Source title
        - Source URL
        - Publication date if available

        Do not invent sources.
        Do not invent URLs.
        """,

        expected_output="""
        A research evidence collection containing:

        - Important findings
        - Supporting evidence
        - Source titles
        - Source URLs
        - Dates where available
        - Conflicting evidence
        """,

        agent=researcher,

        context=[planning_task],
    )

    # -----------------------------------
    # TASK 3 — Fact Checking
    # -----------------------------------

    fact_check_task = Task(
        description="""
        Review the research collected by the previous agent.

        For important claims:

        1. Determine whether the claim is supported.
        2. Check whether the source is relevant.
        3. Identify weak or unsupported claims.
        4. Identify contradictions.
        5. Separate facts from interpretations.
        6. Flag potentially outdated information.

        Do not invent missing evidence.
        """,

        expected_output="""
        A verified evidence summary containing:

        - Supported claims
        - Evidence
        - Source information
        - Unsupported claims
        - Conflicting evidence
        - Limitations
        """,

        agent=fact_checker,

        context=[research_task],
    )

    # -----------------------------------
    # TASK 4 — Writing
    # -----------------------------------

    writing_task = Task(
        description="""
        Write the final research report about:

        {topic}

        Use ONLY the fact-checked evidence from the previous task.

        Use this structure:

        # Research Report

        ## Executive Summary

        ## Introduction

        ## Key Findings

        ## Evidence and Analysis

        ## Different Perspectives

        ## Limitations

        ## Conclusion

        ## Sources

        Rules:

        - Do not invent facts.
        - Do not invent citations.
        - Do not invent URLs.
        - Clearly distinguish evidence from interpretation.
        - Mention uncertainty when evidence is limited.
        - Use the provided sources.
        """,

        expected_output="""
        A complete Markdown research report with:

        - Executive Summary
        - Introduction
        - Key Findings
        - Evidence and Analysis
        - Different Perspectives
        - Limitations
        - Conclusion
        - Sources with URLs
        """,

        agent=writer,

        context=[fact_check_task],
    )

    # -----------------------------------
    # CALLBACK
    # -----------------------------------

    def on_task_complete(task_output):

        if status_callback is None:
            return

        current_agent = getattr(
            task_output,
            "agent",
            ""
        )

        current_agent = str(current_agent).lower()

        if "planner" in current_agent:
            next_agent = "Web Researcher"

        elif "research" in current_agent:
            next_agent = "Fact Checker"

        elif "fact" in current_agent:
            next_agent = "Research Writer"

        else:
            next_agent = "Completed"

        status_callback(
            current_agent,
            next_agent
        )

    # -----------------------------------
    # CREW
    # -----------------------------------

    return Crew(
        agents=[
            planner,
            researcher,
            fact_checker,
            writer,
        ],

        tasks=[
            planning_task,
            research_task,
            fact_check_task,
            writing_task,
        ],

        process=Process.sequential,

        verbose=False,

        task_callback=on_task_complete,

        max_rpm=25,
    )