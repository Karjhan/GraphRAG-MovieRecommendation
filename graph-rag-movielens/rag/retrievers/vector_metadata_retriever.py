from rag.retrievers.vector_retriever import vector_search
from rag.retrievers.graph_retriever import run_cypher

def vector_with_metadata(query):
    results = vector_search(query)

    if not results:
        return []

    ids = [r["movieId"] for r in results]

    cypher = """
    MATCH (m:Movie)
    WHERE m.movieId IN $ids
    OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
    RETURN 
        m.title as title,
        collect(DISTINCT g.name) as genres
    """

    return run_cypher(cypher, {"ids": ids})