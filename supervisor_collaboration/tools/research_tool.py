from crewai.tools import tool

@tool
def research_tool(topic: str) -> str:
    """Simulates research on a given topic and returns insights."""
    print("🔍 research_tool:", topic)
    return f"Research insights about {topic}"