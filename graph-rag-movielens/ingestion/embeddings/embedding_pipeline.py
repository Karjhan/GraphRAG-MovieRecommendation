from qdrant_client.models import Distance, VectorParams, PointStruct
from db.qdrant.client import client

COLLECTION = "movie_embeddings"


def create_collection(vector_size):
    client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )


def upload_embeddings(df, batch_size=256):
    vector_size = len(df.iloc[0].embedding)
    ensure_collection(vector_size)

    points_batch = []

    for i, row in df.iterrows():
        points_batch.append(
            PointStruct(
                id=int(row.movieId),
                vector=row.embedding,
                payload={"movieId": int(row.movieId)}
            )
        )

        if len(points_batch) == batch_size:
            client.upsert(
                collection_name=COLLECTION,
                points=points_batch
            )
            points_batch = []

    if points_batch:
        client.upsert(
            collection_name=COLLECTION,
            points=points_batch
        )

def ensure_collection(vector_size):
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION not in existing:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

def upload_single_embedding(movie_id, embedding):
    ensure_collection(len(embedding))
    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=int(movie_id),
                vector=embedding,
                payload={"movieId": int(movie_id)}
            )
        ]
    )