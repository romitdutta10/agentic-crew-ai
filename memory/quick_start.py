from crewai import Memory

memory = Memory()

# Store -- the LLM infers scope, categories, and importance
memory.remember("We decided to use PostgreSQL for the user database.")

# Retrieve -- results ranked by composite score (semantic + recency + importance)
matches = memory.recall("What database did we choose?")
for m in matches:
    print(f"[{m.score:.2f}] {m.record.content}")

# Tune scoring for a fast-moving project
memory = Memory(recency_weight=0.5, recency_half_life_days=7)

# Forget
memory.forget(scope="/project/old")

# Explore the self-organized scope tree
print(memory.tree())
print(memory.info("/"))