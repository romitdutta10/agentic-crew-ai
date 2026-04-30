from agents.market_agent import market_agent
from models.models import MarketAnalysis
from crewai.tools import tool


@tool
async def market_agent_tool(product: str) -> dict:
    """Tool to analyze market for a given product."""
    print("🤖 Market Agent Tool called")

    query = f"""
    Analyze market for {product}.
    Return:
    - key trends
    - market size
    """

    result = await market_agent.kickoff_async(
        query,
        response_format=MarketAnalysis
    )

    return result.pydantic if result.pydantic else {}