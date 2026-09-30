import os
from typing import Type

import requests
from pydantic import BaseModel, Field

from crewai.tools import BaseTool


class WebSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The web search query to research."
    )


class WebSearchTool(BaseTool):
    name: str = "Web Search"

    description: str = (
        "Search the web for current and relevant information. "
        "Use this tool to find sources, evidence, reports, "
        "official information, and recent research."
    )

    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:

        api_key = os.getenv("SERPER_API_KEY")

        if not api_key:
            return "ERROR: SERPER_API_KEY is not configured."

        try:

            response = requests.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": api_key,
                    "Content-Type": "application/json",
                },
                json={
                    "q": query,
                    "num": 8,
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            results = data.get("organic", [])

            if not results:
                return "No search results were found."

            formatted_results = []

            for index, result in enumerate(results, start=1):

                title = result.get("title", "Untitled")
                link = result.get("link", "")
                snippet = result.get("snippet", "")

                formatted_results.append(
                    f"""
SOURCE {index}

Title: {title}

URL: {link}

Summary:
{snippet}
"""
                )

            return "\n".join(formatted_results)

        except requests.RequestException as error:

            return f"Web search failed: {error}"

        except Exception as error:

            return f"Unexpected search error: {error}"