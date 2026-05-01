from crewai.tools import tool

@tool
def news_tool(topic: str) -> str:
    """Simulates fetching news on a given topic and returns the latest news."""
    print("📰 news_tool:", topic)
    return f"Latest news about {topic}: no major risks"