from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def route_query(question: str):
    prompt = f"""
Classify the query type.

Possible types:
GRAPH → metadata query
VECTOR → semantic search
RECOMMENDATION → movie recommendations

Query:
{question}

Return only one word.
"""
    result = llm.invoke(prompt).strip().upper()

    if "GRAPH" in result:
        return "graph"
    if "VECTOR" in result:
        return "vector"
    return "recommendation"