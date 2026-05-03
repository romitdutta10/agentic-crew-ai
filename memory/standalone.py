from crewai import Memory

memory = Memory()

# Build up knowledge
memory.remember("The API rate limit is 1000 requests per minute.")
memory.remember("Our staging environment uses port 8080.")
memory.remember("The team agreed to use feature flags for all new releases.")

# Later, recall what you need
matches = memory.recall("What are our API limits?", limit=5)
for m in matches:
    print(f"[{m.score:.2f}] {m.record.content}")

# Extract atomic facts from a longer text
raw = """Meeting notes: We decided to migrate from MySQL to PostgreSQL
next quarter. The budget is $50k. Sarah will lead the migration."""

facts = memory.extract_memories(raw)
# ["Migration from MySQL to PostgreSQL planned for next quarter",
#  "Database migration budget is $50k",
#  "Sarah will lead the database migration"]

for fact in facts:
    memory.remember(fact)