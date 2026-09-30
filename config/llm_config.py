import os
from langchain_groq import ChatGroq

# Default model used across all agents
DEFAULT_MODEL = "openai/gpt-oss-120b"

def get_groq_llm(model_name: str = DEFAULT_MODEL):
    """
    Initializes and returns a ChatGroq LLM instance using the provided API key and model name.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing. Please set it in the sidebar or secrets.")
    
    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=0.3
    )