from langchain_core.prompts import PromptTemplate

answer_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a movie expert assistant.

Context:
{context}

Question:
{question}

Answer clearly using the context.
Recommend movies when possible.
"""
)