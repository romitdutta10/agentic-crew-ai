from crewai.tools import tool

@tool
def research_tool(topic: str) -> str:
    """Tool for conducting research on a given topic and returning insights."""
    print("🔧 research_tool called with:", topic)
    return f"""
    Insights on {topic}:
    - AI chatbot market growing rapidly
    - Dominated by OpenAI, Google, Anthropic
    - SaaS adoption increasing
    """

