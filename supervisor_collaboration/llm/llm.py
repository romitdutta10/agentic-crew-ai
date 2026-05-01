# common/llm.py (optional)
from crewai.llm import LLM

groq_llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.7
)

ollama_llm = LLM(
    model="ollama/qwen3:0.6b",
    base_url="http://localhost:11434"
)

openai_llm = LLM(
    # model="groq/llama-3.1-8b-instant",  # stable Groq model
    model="gpt-5.4-nano-2026-03-17",  # stable Groq model
    temperature=0.7
)