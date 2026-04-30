from crewai.agent import Agent

from llm.llm import llm
from tools.research_tool import research_tool

competitor_agent = Agent(
    role="Competitive Analyst",
    goal="Analyze competitors and positioning",
    backstory="Expert in competitor benchmarking and strategy.",
    tools=[research_tool],
    llm=llm,
    verbose=True
)