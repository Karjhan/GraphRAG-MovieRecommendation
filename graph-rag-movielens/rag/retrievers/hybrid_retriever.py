from rag.retrievers.vector_retriever import vector_search
from rag.retrievers.graph_expansion_retriever import expand_from_movies
from rag.retrievers.graph_retriever import get_movies_basic
from rag.services.reranker import rerank_movies

def hybrid_search(query):
    vector_results = vector_search(query, k=20)
    if not vector_results:
        return []

    ids = [r["movieId"] for r in vector_results]
    movies = get_movies_basic(ids)
    top_movies = rerank_movies(query, movies, top_k=5)

    top_ids = [m["movieId"] for m in top_movies]
    return expand_from_movies(top_ids)