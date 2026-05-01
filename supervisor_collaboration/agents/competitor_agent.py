from crewai.agent import Agent
from tools.research_tool import research_tool
from llm.llm import openai_llm

def get_competitor_agent():
    return Agent(
        role="Competitor Analyst",
        goal="Analyze competitors and positioning",
        backstory="Expert in competitive intelligence",
        tools=[research_tool],
        llm=openai_llm,
        verbose=True
    )