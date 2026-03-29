from langchain_core.prompts import PromptTemplate

recommendation_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a movie recommender system.

    User request:
    {question}

    Candidate movies:
    {context}

    STRICT RULES:
    - ONLY recommend movies from the candidate list
    - DO NOT invent movies
    - Use the provided graph context

    Instructions:
    - Recommend 3–5 movies
    - Each recommendation MUST have a DIFFERENT reason
    - Avoid repeating the same explanation
    - Be concise and specific

    Answer:
    """
)