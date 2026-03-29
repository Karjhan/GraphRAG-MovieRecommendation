from qdrant_client import QdrantClient
from config.settings import settings

client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    timeout=60
)