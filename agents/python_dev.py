

import os

from crewai import  Agent, Crew, Process, Task
from crewai.llm import LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff

# from crewai_tools import SerperDevTool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  agents_config = "config/agent_config.yaml"
  tasks_config = 'config/tasks.yaml'

  llm = LLM(
    provider="openai",
    model="mistral",
    api_base=os.getenv("LITELLM_API_BASE", "http://localhost:4000"),
    api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
  )   

  @agent
  def developer(self) -> Agent:
    return Agent(
      config=self.agents_config['developer'], # type: ignore[index]
      verbose=True,
      allow_code_execution=True,
      code_execution_mode="safe",  # Uses Docker for safety
      max_execution_time=300,  # 5-minute timeout
      max_retry_limit=3,  # More retries for complex code tasks
      llm=self.llm
      # tools=[SerperDevTool()]
    )
  
  # @task
  # def development_task(self) -> Task:
  #   return Task(
  #       description="Write Python code based on the topic {topic}",
  #       expected_output="A complete, working Python program",
  #       agent=self.developer()
  #   )

  @task
  def development_task(self) -> Task:
    return Task(
      config=self.tasks_config['development_task'] # type: ignore[index]
    )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=[self.developer()],
      tasks=[self.development_task()],
      process=Process.sequential,
      verbose=True
    )
  
  @before_kickoff
  def prepare_inputs(self, inputs):
      # Modify inputs before the crew starts
      inputs['additional_data'] = "Always run the code with 1 or 2 inputs with numbers in the range 1 to 10"
      return inputs
  
crew = LatestAiDevelopmentCrew()

inputs = {
    "topic": "Write a program in python to add two numbers"  # or whatever input your crew expects
}

result = crew.crew().kickoff(inputs=inputs)

print(result)