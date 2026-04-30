from crewai.tools import tool

from agents.competitor_agent import competitor_agent
from models.models import CompetitorAnalysis

@tool
async def competitor_agent_tool(product: str) -> dict:
    """Tool to analyze competitors for a given product."""
    print("🤖 Competitor Agent Tool called")

    query = f"""
    Analyze competitors for {product}.
    Return:
    - competitors
    - positioning
    """

    result = await competitor_agent.kickoff_async(
        query,
        response_format=CompetitorAnalysis
    )

    return result.pydantic.dict() if result.pydantic else {}