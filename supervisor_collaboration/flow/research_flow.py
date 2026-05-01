import asyncio
from typing import Dict, Any
from pydantic import BaseModel

from crewai.flow.flow import Flow, start, listen
from agents.supervisor_agent import get_supervisor
from registry.agent_registry import (
    market_agent_tool,
    competitor_agent_tool
)
from tools.news_tool import news_tool


class FinalReport(BaseModel):
    summary: str
    market: dict
    competition: dict
    news: str


class ResearchState(BaseModel):
    product: str = ""
    final_report: FinalReport | None = None


class ResearchFlow(Flow[ResearchState]):

    @start()
    def start_flow(self):
        print(f"🚀 Starting for {self.state.product}")
        return {"product": self.state.product}


    @listen(start_flow)
    async def run_hybrid(self):

        product = self.state.product

        print("⚡ Running parallel agents + tools")

        # ✅ Parallel execution (deterministic forcing)
        # market_task = market_agent_tool(product)
        # competitor_task = competitor_agent_tool(product)
        # news_task = asyncio.to_thread(news_tool, product)

        # market, competitor, news = await asyncio.gather(
        #     market_task,
        #     competitor_task,
        #     news_task
        # )

        supervisor = get_supervisor()

        # Supervisor now only merges (controlled intelligence)
        # query = f"""
        # Combine the following into final recommendation:

        # Market:
        # {market}

        # Competitor:
        # {competitor}

        # News:
        # {news}

        # Provide:
        # - summary
        # """

        # Supervisor proposes plan
        query = f"""
            For product: {product}

            Decide:
            - Do we need market analysis?
            - Do we need competitor analysis?
            - Do we need news?

            Based on your decisions, call the relevant tools to get the information you need, and then provide a final summary of the product's market potential.
        """

        result = await supervisor.kickoff_async(query, response_format=ResearchState)

        print("Supervisor decision:", result)

        # return {
        #     "final_report": {
        #         "summary": str(result)
        #         # "market": market,
        #         # "competition": competitor,
        #         # "news": news
        #     }
        # }

        return result


    @listen(run_hybrid)
    def display(self, data):
        report = data["final_report"]

        print("\n📊 FINAL REPORT")
        print("=" * 40)
        print("Summary:", report["summary"])
        print("Market:", report["market"])
        print("Competition:", report["competition"])
        print("News:", report["news"])