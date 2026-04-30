from crewai.agent import Agent

from agent_as_tool.competitor_agent_tool import competitor_agent_tool
from agent_as_tool.market_agent_as_tool import market_agent_tool

from llm.llm import llm
from tools.research_tool import research_tool

supervisor_agent = Agent(
    role="Strategy Supervisor",
    goal="Coordinate market and competitor analysis and produce final report",
    backstory="Senior strategist who combines multiple analyses into decisions.",
    tools=[market_agent_tool, competitor_agent_tool],
    llm=llm,
    verbose=True
)