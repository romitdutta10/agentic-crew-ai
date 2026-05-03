from crewai.tools import tool
from crewai import  Agent, Crew, Process, Task
from crewai.llm import LLM


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

@tool
def multiplication_tool(first_number: int, second_number: int) -> str:
    """Useful for when you need to multiply two numbers together."""
    return first_number * second_number

def cache_func(args, result):
    # In this case, we only cache the result if it's a multiple of 2
    print(f"Caching result: {result} for args: {args}")
    cache = result % 2 == 0
    return cache

multiplication_tool.cache_function = cache_func

writer1 = Agent(
        role="Writer",
        goal="You write lessons of math for kids.",
        backstory="You're an expert in writing and you love to teach kids but you know nothing of math.",
        tools=[multiplication_tool],
        allow_delegation=False,
        llm=groq_llm,
        verbose=True
    )

# Create a task that requires code execution
research_analysis_task = Task(
    description="Multiply 2 and 2",
    expected_output="The result of the multiplication.",
    agent=writer1
)

research_analysis_task_2 = Task(
    description="Multiply 2 with 2",
    expected_output="The result of the multiplication.",
    agent=writer1
)

# Create a crew and add the task
analysis_crew = Crew(
    agents=[writer1],
    tasks=[research_analysis_task, research_analysis_task_2],
    verbose=True,
)

# Execute the crew
result = analysis_crew.kickoff()

print(result)