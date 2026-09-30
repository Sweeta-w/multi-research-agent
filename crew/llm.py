import os

from crewai import LLM


def get_llm():
    """Create the Groq LLM used by all research agents."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    return LLM(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        custom_openai=True,
        temperature=0.2,
    )