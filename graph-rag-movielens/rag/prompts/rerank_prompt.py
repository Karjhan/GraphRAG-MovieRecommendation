from langchain_core.prompts import PromptTemplate

rerank_prompt = PromptTemplate(
    input_variables=["query", "movie"],
    template="""
You are a ranking model.

Task:
Score how relevant the movie is to the user query.

Query:
{query}

Movie:
{movie}

Rules:
- Return ONLY a number between 0 and 10
- 10 = highly relevant
- 0 = not relevant
- Do NOT explain

Score:
"""
)