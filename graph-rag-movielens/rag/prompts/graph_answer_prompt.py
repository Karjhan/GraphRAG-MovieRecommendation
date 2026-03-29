from langchain_core.prompts import PromptTemplate

graph_answer_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a strict data assistant.

Answer ONLY using the provided context.

STRICT RULES:
- DO NOT recommend movies
- DO NOT add extra suggestions
- DO NOT use outside knowledge
- If the answer is not in context, say "Not found"

Context:
{context}

Question:
{question}

Answer:
"""
)