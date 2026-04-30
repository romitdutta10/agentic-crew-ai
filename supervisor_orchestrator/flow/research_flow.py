from crewai.flow.flow import Flow, start, listen
from typing import Dict, Any
from pydantic import BaseModel, Field
from typing import List, Optional

from agents.supervisor_agent import supervisor_agent
from models.models import FinalReport

class ResearchState(BaseModel):
    product: str = ""
    final_report: Optional[FinalReport] = None


class ResearchFlow(Flow[ResearchState]):

    @start()
    def start_flow(self) -> Dict[str, Any]:
        print(f"🚀 Starting research for {self.state.product}")
        return {"product": self.state.product}
    
    def _build_query(self):
        return f"""
        Product: {self.state.product}

        STRICT INSTRUCTIONS:
        1. Call market_agent_tool
        2. Call competitor_agent_tool
        3. Combine outputs

        You are FORBIDDEN from answering without tools.

        If you skip tools, your response will be rejected.
        """


    @listen(start_flow)
    async def run_supervisor(self) -> Dict[str, Any]:

        query = f"""
                You are NOT allowed to answer from your own knowledge.

                You MUST follow this exact sequence:

                Step 1:
                Call `market_agent_tool` with product = "{self.state.product}"

                Step 2:
                Call `competitor_agent_tool` with product = "{self.state.product}"

                Step 3:
                Combine both results into final output.

                Rules:
                - DO NOT skip tool calls
                - DO NOT fabricate data
                - If tools are not called, the answer is INVALID
                - Final answer MUST be based ONLY on tool outputs

                Return structured response.

                You DO NOT have access to:
                - market trends
                - competitors

                These MUST come from tools.
                """

        # result = await supervisor_agent.kickoff_async(
        #     query,
        #     response_format=FinalReport
        # )

        # if result.pydantic:
        #     print("✅ Final structured output ready")
        #     return {"final_report": result.pydantic}

        # print("⚠️ Fallback to raw result")
        # return {"final_report": None}

        for attempt in range(3):  # retry loop

            print(f"\n🔁 Supervisor attempt {attempt+1}")

            result = await supervisor_agent.kickoff_async(
                self._build_query(),
                response_format=FinalReport
            )

            if result.pydantic:
                report = result.pydantic

                # ✅ HARD CHECK: ensure tool outputs exist
                if report.market and report.competition:
                    print("✅ Tools were used properly")
                    return {"final_report": report}

            print("❌ Tools not used properly. Retrying...")

        raise Exception("Supervisor failed to use tools after retries")


    @listen(run_supervisor)
    def display(self, data):
        report = data.get("final_report")

        print("\n📊 FINAL REPORT")
        print("=" * 40)

        if not report:
            print("No structured report generated")
            return

        print("\n📈 Market Trends:")
        for t in report.market.key_trends:
            print("-", t)

        print("\n💰 Market Size:", report.market.market_size)

        print("\n🏆 Competitors:")
        for c in report.competition.competitors:
            print("-", c)

        print("\n🧭 Summary:")
        print(report.summary)