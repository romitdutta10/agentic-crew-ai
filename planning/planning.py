from crewai import Agent, Crew, Task, Process, LLM
# from crewai_tools import YourCustomTool

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",  # stable Groq model
    temperature=0
)

ollama_llm = LLM(
    model="ollama/qwen3:0.6b",
    base_url="http://localhost:11434"
)

openai_llm = LLM(
    # model="groq/llama-3.1-8b-instant",  # stable Groq model
    model="gpt-5.4-nano-2026-03-17",  # stable Groq model
    # temperature=0.7
)

class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics",
            verbose=True,
            llm=ollama_llm,
            # tools=[YourCustomTool()]
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail",
            verbose=True,
            llm=ollama_llm
        )

    def task_one(self) -> Task:
        return Task(
            description="Collect recent market data and identify trends.",
            expected_output="A report summarizing key trends in the market. Ensure the report is within 100 words",
            # agent=self.agent_one()
        )

    def task_two(self) -> Task:
        return Task(
            description="Research factors affecting market dynamics.",
            expected_output="An analysis of factors influencing the market. Ensure the analysis is within 100 words.",
            # agent=self.agent_two()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            # process=Process.sequential,
            process=Process.hierarchical,
            verbose=True,
            planning=True,
            planning_llm=openai_llm,
            manager_llm=openai_llm
        )
    
if __name__ == "__main__":
    crew_instance = YourCrewName().crew()
    result = crew_instance.kickoff()
    print(result)