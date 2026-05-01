from crewai.agent import Agent
from llm.llm import openai_llm
from registry.tool_registry import get_all_tools

def get_supervisor():
    return Agent(
        role="Vendor Strategy Supervisor",
        goal="Evaluate vendors using agents and tools",
        backstory="Expert decision maker who chooses best data sources",
        tools=get_all_tools(),
        llm=openai_llm,
        verbose=True
    )