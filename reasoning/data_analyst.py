from crewai import Agent, Task, Crew, LLM

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",  # stable Groq model
    temperature=0
)
# Create an agent with reasoning enabled
analyst = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    backstory="You are an expert data analyst.",
    reasoning=True,
    max_reasoning_attempts=3,  # Optional: Set a limit on reasoning attempts
    llm=groq_llm,
    verbose=True
)

# Create a task
analysis_task = Task(
    description="Analyze the provided sales data and identify key trends.",
    expected_output="A report highlighting the top 3 sales trends.",
    agent=analyst
)

# Create a crew and run the task
crew = Crew(agents=[analyst], tasks=[analysis_task])
result = crew.kickoff()

print(result)