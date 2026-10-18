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

        Create a focused and concise research plan.

        Identify:

        1. The main research question.
        2. Important subtopics.
        3. Specific questions that need answers.
        4. Useful search keywords.
        5. Types of evidence that should be collected.

        Keep the plan focused so unnecessary searches are avoided.

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

        Use the available web search tool to find reliable
        and relevant evidence.

        Prioritize:

        - Official organizations
        - Government sources
        - Academic sources
        - Research institutions
        - Reputable reports
        - Recent information

        Focus on useful evidence rather than collecting a large
        number of repetitive sources.

        For every important finding, record:

        - Claim
        - Evidence or search-result snippet
        - Source title
        - Exact source URL returned by the web search tool
        - Publication date if available
        - Source type if it can be determined from the search result

        IMPORTANT SOURCE RULES:

        - Preserve the exact source URL returned by the web search tool.
        - Never invent or modify a URL.
        - Never invent a source title.
        - Treat search-result summaries as snippets, not as the full
          content of an article, report, or research paper.
        - Do not claim that a full source was reviewed when only a
          search-result snippet was available.
        - If a date or other source detail is unavailable, say
          "Not available" instead of guessing.
        - Keep source information attached to the claim it supports.
        - Do not invent evidence.
        """,

        expected_output="""
        A concise research evidence collection.

        For important findings use this format:

        CLAIM:
        The important factual claim.

        EVIDENCE:
        The evidence or search-result snippet supporting the claim.

        SOURCE TITLE:
        The exact source title returned by web search.

        SOURCE URL:
        The exact source URL returned by web search.

        DATE:
        Publication date if available, otherwise "Not available".

        SOURCE TYPE:
        Government, academic, official organization, research
        institution, reputable report, news, or other when identifiable.

        Include:

        - Important findings
        - Supporting evidence
        - Source titles
        - Source URLs
        - Dates where available
        - Conflicting evidence where found

        Do not create source information that was not returned
        by the web search tool.
        """,

        agent=researcher,

        context=[planning_task],
    )

    # -----------------------------------
    # TASK 3 — Fact Checking
    # -----------------------------------

    fact_check_task = Task(
        description="""
        Review the research evidence collected by the previous agent.

        Evaluate the evidence that was actually provided.

        For each important claim:

        1. Determine whether the provided evidence supports the claim.
        2. Check whether the provided source is relevant to the claim.
        3. Identify weak or unsupported claims.
        4. Identify contradictions in the collected evidence.
        5. Separate factual evidence from interpretation.
        6. Flag potentially outdated information when this can be
           determined from the provided evidence.
        7. Preserve the source title and source URL associated with
           each evaluated claim.

        Classify important claims as:

        - SUPPORTED
        - WEAK
        - CONTRADICTED
        - UNVERIFIED

        IMPORTANT:

        You are evaluating the evidence supplied by the researcher.

        Do not pretend that you independently opened or read a source
        when only a search-result snippet was provided.

        Do not use your own memory as evidence.

        Do not invent missing evidence.

        Do not invent citations, source titles, publication dates,
        authors, or URLs.

        If the available evidence is insufficient, classify the claim
        as WEAK or UNVERIFIED rather than guessing.
        """,

        expected_output="""
        A concise verified evidence summary.

        For each major claim include:

        CLAIM:
        The claim being evaluated.

        STATUS:
        SUPPORTED / WEAK / CONTRADICTED / UNVERIFIED

        EVIDENCE:
        The evidence that was actually provided.

        SOURCE TITLE:
        Original source title if provided.

        SOURCE URL:
        Original source URL if provided.

        REASON:
        A short explanation of the verification decision.

        Also identify:

        - Conflicting evidence
        - Important limitations
        - Missing evidence

        Preserve source information from the research task.
        Do not create new source information.
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

        You have access to:

        1. The original research evidence and source information.
        2. The fact checker's evaluation of that evidence.

        Use the fact checker's decisions when deciding which claims
        are reliable enough to include.

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

        RULES:

        - Use only evidence supplied by the research process.
        - Give preference to claims classified as SUPPORTED.
        - Clearly identify uncertainty around WEAK or UNVERIFIED claims.
        - Do not present CONTRADICTED claims as established facts.
        - Clearly distinguish evidence from interpretation.
        - Mention uncertainty when evidence is limited.

        SOURCE AND CITATION RULES:

        - Use only source titles and URLs that appear in the original
          research evidence.
        - Never invent a source.
        - Never invent a URL.
        - Never invent an author or publication date.
        - Never create citation markers or line references that were
          not supplied by the research evidence.
        - Do not generate citation formats such as [1], (1), or
          line-reference markers unless they correspond to actual
          provided source information.
        - If a claim cannot be traced to provided evidence, either
          clearly label it as unverified or omit it.
        - In the Sources section, list the actual source title together
          with its provided URL.
        - Do not claim to have read a complete webpage, paper, or report
          when the available evidence came only from a search snippet.
        """,

        expected_output="""
        A complete Markdown research report containing:

        - Executive Summary
        - Introduction
        - Key Findings
        - Evidence and Analysis
        - Different Perspectives
        - Limitations
        - Conclusion
        - Sources

        Every important factual claim should be traceable to source
        information contained in the original research evidence.

        The Sources section must contain only source titles and URLs
        actually supplied by the research task.
        """,

        agent=writer,

        # IMPORTANT:
        # Writer receives both the original evidence and the
        # fact-checker's evaluation.
        context=[
            research_task,
            fact_check_task,
        ],
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
