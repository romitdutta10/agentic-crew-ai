from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai import Agent, Task, Crew, Process, LLM
import os

target = "Animals.txt"
text_source = TextFileKnowledgeSource(
    file_paths=[target]
)


# target = "sources\Animals.txt"
# print(f"Checking path: {os.path.abspath(target)}")
# print(f"File exists: {os.path.exists(target)}")

# raise FileNotFoundError(f"File not found at path: {os.path.abspath(target)}")


groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",  # stable Groq model
    temperature=0
)

# Create an agent with the knowledge store
agent = Agent(
    role="About Text",
    goal="You know everything about the text.",
    backstory="You are a master at understanding text and their content.",
    verbose=True,
    allow_delegation=False,
    llm=groq_llm,
)

task = Task(
    description="Answer the following questions about the text: {question}",
    expected_output="An answer to the question.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[text_source], # Enable knowledge by adding the sources here,
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}}
)

result = crew.kickoff(inputs={"question": "Among the animal species, how many are vertebrates?"})