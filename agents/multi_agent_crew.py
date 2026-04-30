from crewai import Agent, Crew, Task, Process
# from crewai_tools import YourCustomTool
from crewai.llm import LLM
from crewai.tools import tool

# Groq LLM
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.7
)

@tool
def research_tool(topic: str) -> str:
    """Research tool which is useful for when you need to gather information on a specific topic."""
    print("Tool called with topic:", topic)
    # This is a placeholder implementation - replace with actual research logic
    return f"Research results for {topic}: A chatbot (originally chatterbot)[1] is a software application or web interface designed to converse through text or speech.[2][3][4] Modern chatbots are typically online and use generative artificial intelligence systems that are capable of maintaining a conversation with a user in natural language and simulating the way a human would behave as a conversational partner. Such chatbots often use deep learning and natural language processing. Simpler chatbots have existed for decades. Chatbots have gained popularity with the release of ChatGPT by OpenAI in 2022, followed by competitors such as Gemini, Claude, and Grok, in what is labelled an AI boom.AI chatbots typically use fine-tuned large language models to generate text. A major area where chatbots have long been used is customer service and support, with various sorts of virtual assistants."



class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics",
            verbose=True,
            tools=[research_tool],
            llm=llm
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail",
            verbose=True,
            llm=llm
        )

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
    

YourCrewName().crew().kickoff(inputs={"topic": "Do a market research on AI powered chatbots"})