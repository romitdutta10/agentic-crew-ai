from crewai.tools import tool
from agents.market_agent import get_market_agent
from agents.competitor_agent import get_competitor_agent

market_agent = get_market_agent()
competitor_agent = get_competitor_agent()


@tool
async def market_agent_tool(product: str) -> dict:
    """Simulates market analysis for a given product and returns insights."""
    print("🤖 market_agent_tool called")

    result = await market_agent.kickoff_async(
        f"Analyze market for {product}",
    )

    return {"market_raw": str(result)}


@tool
async def competitor_agent_tool(product: str) -> dict:
    """Simulates competitor analysis for a given product and returns insights."""
    print("🤖 competitor_agent_tool called")

    result = await competitor_agent.kickoff_async(
        f"Analyze competitors for {product}",
    )

    return {"competitor_raw": str(result)}