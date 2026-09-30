import os
from crewai import LLM

def get_groq_llm(model_name: str = "groq/openai/gpt-oss-120b"):
    """
    Initializes CrewAI native LLM instance for Groq.
    Format: 'groq/<model_name>'
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing.")
    
    # Ensure provider prefix is present
    if not model_name.startswith("groq/"):
        model_name = f"groq/{model_name}"
        
    return LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.3
    )