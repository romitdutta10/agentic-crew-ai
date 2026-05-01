from tools.research_tool import research_tool
from tools.news_tool import news_tool
from registry.agent_registry import (
    market_agent_tool,
    competitor_agent_tool
)

def get_all_tools():
    return [
        market_agent_tool,
        competitor_agent_tool,
        research_tool,
        news_tool
    ]