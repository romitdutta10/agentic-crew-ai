import asyncio
from typing import Any, Dict, List

from crewai_tools import SerperDevTool
from crewai.tools import tool
from pydantic import BaseModel, Field
import os
from crewai.agent import Agent
from crewai.flow.flow import Flow, listen, start
from crewai.llm import LLM


# Define a structured output format
class MarketAnalysis(BaseModel):
    key_trends: List[str] = Field(description="List of identified market trends")
    market_size: str = Field(description="Estimated market size")
    competitors: List[str] = Field(description="Major competitors in the space")


# Define flow state
class MarketResearchState(BaseModel):
    product: str = ""
    analysis: MarketAnalysis | None = None

@tool
def research_tool(topic: str) -> str:
    """Research tool which is useful for when you need to gather information on a specific topic."""
    print("Tool called with topic:", topic)
    # This is a placeholder implementation - replace with actual research logic
    return f"Research results for {topic}: A chatbot (originally chatterbot)[1] is a software application or web interface designed to converse through text or speech.[2][3][4] Modern chatbots are typically online and use generative artificial intelligence systems that are capable of maintaining a conversation with a user in natural language and simulating the way a human would behave as a conversational partner. Such chatbots often use deep learning and natural language processing. Simpler chatbots have existed for decades. Chatbots have gained popularity with the release of ChatGPT by OpenAI in 2022, followed by competitors such as Gemini, Claude, and Grok, in what is labelled an AI boom.AI chatbots typically use fine-tuned large language models to generate text. A major area where chatbots have long been used is customer service and support, with various sorts of virtual assistants."


@tool
def weather_tool(region: str) -> str:
    """Useful for when you need to gather weather information for a specific region."""
    print("Tool called with region:", region)
    # This is a placeholder implementation - replace with actual weather logic
    return f"Weather results for {region}: Sunny and warm."


# Create a flow class
class MarketResearchFlow(Flow[MarketResearchState]):
    @start()
    def initialize_research(self) -> Dict[str, Any]:
        print(f"Starting market research for {self.state.product}")
        return {"product": self.state.product}

    
    @listen(initialize_research)
    async def analyze_market(self) -> Dict[str, Any]:

        # llm = LLM(
        #     provider="openai",
        #     model="qwen3",
        #     api_base=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
        #     api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
        # ) 

        # Groq LLM
        llm = LLM(
            model="groq/llama-3.1-8b-instant",
            temperature=0.7
        )
        # Create an Agent for market research
        analyst = Agent(
            role="Market Research Analyst",
            goal=f"Analyze the market for {self.state.product} by only using the above research tool to gather information and provide insights.",
            backstory="You are an experienced market analyst with expertise in "
            "identifying market trends and opportunities.",
            tools=[research_tool],
            verbose=True,
            llm=llm
        )

        # Define the research query
        query = f"""
        Research the market for {self.state.product}. Include:
        1. Key market trends
        2. Market size
        3. Major competitors

        Format your response according to the specified structure.
        """

        # Execute the analysis with structured output format
        result = await analyst.kickoff_async(query, response_format=MarketAnalysis)
        if result.pydantic:
            print("result", result.pydantic)
        else:
            print("result", result)

        # Return the analysis to update the state
        return {"analysis": result.pydantic}

    @listen(analyze_market)
    def present_results(self, analysis) -> None:
        print("\nMarket Analysis Results")
        print("=====================")

        if isinstance(analysis, dict):
            # If we got a dict with 'analysis' key, extract the actual analysis object
            market_analysis = analysis.get("analysis")
        else:
            market_analysis = analysis

        if market_analysis and isinstance(market_analysis, MarketAnalysis):
            print("\nKey Market Trends:")
            for trend in market_analysis.key_trends:
                print(f"- {trend}")

            print(f"\nMarket Size: {market_analysis.market_size}")

            print("\nMajor Competitors:")
            for competitor in market_analysis.competitors:
                print(f"- {competitor}")
        else:
            print("No structured analysis data available.")
            print("Raw analysis:", analysis)
 

# Usage example
async def run_flow():
    flow = MarketResearchFlow()
    # flow.plot("MarketResearchFlowPlot")
    result = await flow.kickoff_async(inputs={"product": "AI-powered chatbots"})
    return result


# Run the flow
if __name__ == "__main__":
    asyncio.run(run_flow())