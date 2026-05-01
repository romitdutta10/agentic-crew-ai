from crewai.agent import Agent

from llm.llm import groq_llm
from tools.research_tool import research_tool

market_agent = Agent(
    role="Market Intelligence Analyst",
    goal="Analyze market trends and size",
    backstory="Expert in market research and industry trends.",
    tools=[research_tool],
    llm=groq_llm,
    verbose=True
)