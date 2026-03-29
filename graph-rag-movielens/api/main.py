from fastapi import FastAPI
from ingestion.run_ingestion import run_ingestion
from api.routes.ingest_entry import router as ingest_entry_router
from api.routes.query import router as query_router
from api.routes import vector_query

app = FastAPI()
app.include_router(ingest_entry_router, prefix="/ingest")
app.include_router(query_router, prefix="/query")
app.include_router(vector_query.router, prefix="/vector-query")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/admin/ingest")
def ingest():

    run_ingestion()

    return {"status": "ingestion complete"}