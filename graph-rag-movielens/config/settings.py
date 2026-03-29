from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    MOVIES_PATH: str = "data/processed/movies_clean.csv"
    EMBEDDINGS_PATH: str = "data/processed/embeddings.parquet"

settings = Settings()