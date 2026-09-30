"""
Agents Package
Contains modular definitions for CrewAI agents:
- Researcher
- Analyst
- Writer
"""

from .researcher import create_researcher_agent
from .analyst import create_analyst_agent
from .writer import create_writer_agent

__all__ = [
    "create_researcher_agent",
    "create_analyst_agent",
    "create_writer_agent",
]