from crewai.llm import LLM

llm = LLM(
    # model="groq/llama-3.1-8b-instant",  # stable Groq model
    model="gpt-5.4-nano-2026-03-17",  # stable Groq model
    temperature=0.7
)

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",  # stable Groq model
    temperature=0.7
)