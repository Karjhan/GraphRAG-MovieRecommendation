from ingestion.embeddings.embedding_pipeline import COLLECTION
from ingestion.embeddings.embedding_service import generate_embedding
from db.qdrant.client import client

def vector_search(query, k=20):
    embedding = generate_embedding(query)
    results = client.search(
        collection_name=COLLECTION,
        query_vector=embedding,
        limit=k
    )
    return [
        {
            "movieId": hit.payload["movieId"],
            "score": hit.score
        }
        for hit in results
    ]