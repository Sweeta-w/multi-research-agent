import os
from crewai import LLM

def get_groq_llm(model_name: str = "groq/llama-3.3-70b-versatile"):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing.")
    
    # Ensure provider prefix is present for LiteLLM routing
    if not model_name.startswith("groq/"):
        model_name = f"groq/{model_name}"
        
    return LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.3
    )