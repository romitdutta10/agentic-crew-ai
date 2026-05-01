from crewai import Agent, Crew, Task, Process
from crewai.llm import LLM

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",  # stable Groq model
    temperature=0.7
)


ollama_llm = LLM(
    model="ollama/qwen3:0.6b",
    base_url="http://localhost:11434"
)

# Create collaborative agents
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate, up-to-date information on any topic within 100 words",
    backstory="""You're a meticulous researcher with expertise in finding 
    reliable sources and fact-checking information across various domains.""",
    allow_delegation=True,
    verbose=True,
    llm=groq_llm
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging, well-structured content within 100 words",
    backstory="""You're a skilled content writer who excels at transforming 
    research into compelling, readable content for different audiences.""",
    allow_delegation=True,
    verbose=True,
    llm=ollama_llm
)

editor = Agent(
    role="Content Editor",
    goal="Ensure content quality and consistency within 100 words",
    backstory="""You're an experienced editor with an eye for detail, 
    ensuring content meets high standards for clarity and accuracy.""",
    allow_delegation=True,
    verbose=True,
    llm=ollama_llm
)

# Create a task that encourages collaboration
article_task = Task(
    description="""Write a comprehensive 100-word article about 'The Future of AI in Healthcare'.
    
    The article should include:
    - Current AI applications in healthcare
    
    Collaborate with your teammates to ensure accuracy and quality.""",
    expected_output="A well-researched, engaging 100-word article with proper structure and citations",
    agent=writer  # Writer leads, but can delegate research to researcher
)

# Create collaborative crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[article_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()