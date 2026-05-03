from crewai import Agent, Memory, Crew, Task, Process, LLM

memory = Memory()

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",  # stable Groq model
    temperature=0.7
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

# Researcher gets a private scope -- only sees /agent/researcher
researcher = Agent(
    role="Researcher",
    goal="Find and analyze information",
    backstory="Expert researcher with attention to detail",
    memory=memory.scope("/agent/researcher"),
    llm=groq_llm,
    allow_delegation=False,
    tools=[]
)

# Writer uses crew shared memory (no agent-level memory set)
writer = Agent(
    role="Writer",
    goal="Produce clear, well-structured content",
    backstory="Experienced technical writer",
    llm=groq_llm,
    allow_delegation=False,
    tools=[],
    # memory not set -- uses crew._memory when crew has memory enabled
)

writing_task =  Task(
            description="Based on your knowledge, summarize recent market trends and identify key patterns affecting market growth.",
            expected_output="A report summarizing key trends in the market. Ensure the report is within 100 words",
            agent=writer
        )

research_task = Task(
        description="Based on your knowledge, analyze the primary factors influencing market dynamics and economic conditions.",
        expected_output="An analysis of factors influencing the market. Ensure the analysis is within 100 words.",
        agent=researcher
    )

# Option 1: Default memory
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    memory=True,
    verbose=True,
)

# Option 2: Custom memory with tuned scoring
# memory = Memory(
#     recency_weight=0.4,
#     semantic_weight=0.4,
#     importance_weight=0.2,
#     recency_half_life_days=14,
# )
# crew = Crew(
#     agents=[researcher, writer],
#     tasks=[research_task, writing_task],
#     memory=memory,
# )


result = crew.kickoff()
print(result)