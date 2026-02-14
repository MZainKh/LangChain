from dotenv import load_dotenv
load_dotenv()

from fastmcp import FastMCP
from tavily import TavilyClient
from typing import Dict, Any
from requests import get

mcp = FastMCP[any]("mcp-server")

tavily_client = TavilyClient()

@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """search the web for information."""
    results = tavily_client.search(query)

    return results

@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    """read the README file from the langchain-mcp-adapters repository."""
    url = f"https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/blob/main/README.md"
    try: 
        response = get(url)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.prompt()
def prompt():
    """Analyze data from langchain-ai repo file with comprehensive summary"""
    return """
        You are a helpful assistant that answers user questions about LangChain, LangGraph, and LangSmith. 

        You can use the following tools/resources to answer user questions:
        - search_web: Search the web for information.
        - github_file: Access the langchain-ai repository file.

        If the user asks a question that is not related to LangChain, LangGraph, or LangSmith, you should say "I'm sorry, I don't know how to answer that question."

        You may try multiple tool and resource calls to answer the user's question.

        You may also ask clarifying questions to the user to better understand their question.
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")
