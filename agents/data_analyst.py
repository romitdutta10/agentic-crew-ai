from crewai import Agent, Crew, Task, Process
from crewai.tools import tool
from crewai.llm import LLM
import os

class YourCrewName:

    llm = LLM(
    provider="openai",
    model="mistral",
    api_base=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
    api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
    )   
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics who can only use tools to retrieve information",
            verbose=True,
            tools=[self.data_analysis],
            llm=self.llm
        )

    @tool
    def data_analysis(self, topic) -> str:
        """Do data analysis on the given topic and return insights."""
        # This is where you would implement the logic for data analysis
        # For demonstration, we'll return a placeholder string
        return f"Data analysis results: {topic}"



    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail ho can only use tools to retrieve information",
            verbose=True,
            llm=self.llm,
            tools=[self.market_research]
        )
    
    @tool
    def market_research(self, topic) -> str:
        """Gather information on market dynamics and return findings."""
        # This is where you would implement the logic for market research
        # For demonstration, we'll return a placeholder string
        return f"Market research findings: {topic}"

    def task_one(self) -> Task:
        return Task(
            description="Collect recent market data and identify trends.",
            expected_output="A report summarizing key trends in the market.",
            agent=self.agent_one()
        )

    def task_two(self) -> Task:
        return Task(
            description="Research factors affecting market dynamics.",
            expected_output="An analysis of factors influencing the market.",
            agent=self.agent_two()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            process=Process.sequential,
            verbose=True
        )
    

YourCrewName().crew().kickoff(inputs={})