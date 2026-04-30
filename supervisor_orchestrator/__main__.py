import asyncio

from flow.research_flow import ResearchFlow

async def main():
    flow = ResearchFlow()
    await flow.kickoff_async(inputs={
        "product": "AI-powered chatbots"
    })

if __name__ == "__main__":
    asyncio.run(main())