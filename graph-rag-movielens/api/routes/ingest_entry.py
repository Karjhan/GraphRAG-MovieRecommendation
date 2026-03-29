from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, conlist
from db.neo4j.connection import Neo4jConnection
from ingestion.graph_builder.node_builder import NodeBuilder
from ingestion.graph_builder.relationship_builder import RelationshipBuilder
from ingestion.embeddings.embedding_pipeline import client, COLLECTION, VectorParams, Distance, upload_single_embedding
from ingestion.embeddings.embedding_service import generate_embedding

router = APIRouter()

class MovieEntry(BaseModel):
    movieId: int
    title: str
    genres: conlist(str, min_length=1)
    overview: str = ""
    embedding_text: str

@router.post("/entry")
def ingest_entry(movie: MovieEntry):
    node_builder = NodeBuilder()
    rel_builder = RelationshipBuilder()

    node_builder.create_movie({
        "movieId": movie.movieId,
        "title": movie.title,
        "overview": movie.overview
    })

    for genre in movie.genres:
        node_builder.create_genre(genre)
        rel_builder.link_movie_genre(movie.movieId, genre)

    embedding = generate_embedding(movie.embedding_text)
    upload_single_embedding(movie.movieId, embedding)

    return {"status": "success", "movieId": movie.movieId}