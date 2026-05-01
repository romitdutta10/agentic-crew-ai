from crewai.agent import Agent
from tools.research_tool import research_tool
from llm.llm import openai_llm

def get_market_agent():
    return Agent(
        role="Market Analyst",
        goal="Analyze market trends and size",
        backstory="Expert in market intelligence",
        tools=[research_tool],
        llm=openai_llm,
        verbose=True
    )