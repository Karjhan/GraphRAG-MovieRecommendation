from langchain_core.prompts import PromptTemplate

cypher_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are an expert in Neo4j Cypher queries.

Graph schema:

(:Movie {title, overview, movieId})
(:Genre {name})

Relationships:
(:Movie)-[:HAS_GENRE]->(:Genre)

Rules:
- Generate ONLY valid Cypher
- Do NOT include explanations
- Use only the schema provided
- Prefer simple and efficient queries

User question:
{question}

Cypher query:
"""
)