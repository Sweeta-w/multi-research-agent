import os
import streamlit as st
from crewai import LLM

def get_groq_llm(model_name: str = "groq/llama-3.3-70b-versatile"):
    # 1. First check os.environ, then fallback to Streamlit Secrets
    api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY missing. Please set it in Streamlit Secrets or Sidebar.")
    
    # Explicitly set for LiteLLM child threads
    os.environ["GROQ_API_KEY"] = api_key
    
    if not model_name.startswith("groq/"):
        model_name = f"groq/{model_name}"
        
    return LLM(
        model=model_name,
        api_key=api_key,
        temperature=0.3
    )