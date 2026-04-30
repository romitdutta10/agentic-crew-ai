import os

from crewai import Agent, Task, Crew
from crewai.llm import LLM
from langchain_ollama import OllamaLLM
from openai import OpenAI
from dotenv import load_dotenv
import litellm




# from ollama import chat

# response = chat(
#     model='mistral',
#     messages=[{'role': 'user', 'content': 'Hello!'}],
# )
# print(response.message.content)

load_dotenv()  # Load environment variables from .env file

litellm.api_base = os.getenv("LITELLM_API_BASE")  # Point to your LiteLLM proxy
litellm.api_key = os.getenv("LITELLM_MASTER_KEY")  # Your master_key from config.yaml

# print(litellm.version)

model_name = "mistral"

# Create an Ollama LLM instance
# Initialize the model
# llm = OllamaLLM(model=model_name)

# Invoke the model
# response = llm.invoke("Why is the sky blue?")
# print(response)

# litellm_model_name = "mistral"  # Prefix with "ollama/" for local models

# messages = [
# {"role": "system", "content": "You are a helpful assistant."},
# {"role": "user", "content": "Why is the sky blue?"}
# ]

# # response = litellm.completion(
# #     model=litellm_model_name,
# #     messages=messages,
# #     stream=False
# # )

# # print(response['choices'][0]['message']['content'])

# # Connect to LiteLLM proxy (which has OpenAI-compatible API)
# client = OpenAI(
#     base_url=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
#     api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
# )


# # Use OpenAI client to talk to LiteLLM proxy
# response = client.chat.completions.create(
#     model="mistral",  # Model name from your config.yaml
#     messages=messages,
#     stream=True
# )

# # print("Response:")


# print("Response:")
# for chunk in response:
#     if chunk.choices[0].delta.content:
#         print(chunk.choices[0].delta.content, end='', flush=True)
# print()

# Create LLM configured for LiteLLM
# llm = LLM(
#     provider="litellm",
#     model="ollama/mistral",
#     api_base=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
#     api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
# )
llm = LLM(
    provider="openai",
    model="mistral",
    api_base=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
    api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
)

# Create an agent with code execution enabled
# coding_agent = Agent(
#     role="Python Data Analyst",
#     goal="Analyze data and provide insights using Python",
#     backstory="You are an experienced data analyst with strong Python skills.",
#     allow_code_execution=True,
#     # llm=litellm.completion,
#     # model="mistral"  # Your model name from config.yaml
#     llm=llm
# )
# Create an agent with code execution enabled
researcher_agent = Agent(
    role="Senior Data Researcher",
    goal="Uncover cutting-edge developments in any topic",
    backstory="You're a seasoned researcher with a knack for uncovering the latest developments in any topic. Known for your ability to find the most relevant information and present it in a clear and concise manner.",
    allow_code_execution=False,
    # llm=litellm.completion,
    # model="mistral"  # Your model name from config.yaml
    llm=llm
)

# Create a task that requires code execution
research_analysis_task = Task(
    description="Research about the job landscape in India",
    expected_output="A detailed analysis including the average pay and companies available",
    agent=researcher_agent
)

# Create a crew and add the task
analysis_crew = Crew(
    agents=[researcher_agent],
    tasks=[research_analysis_task]
)

# Execute the crew
result = analysis_crew.kickoff()

print(result)