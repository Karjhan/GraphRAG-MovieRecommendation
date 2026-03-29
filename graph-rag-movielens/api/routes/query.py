from fastapi import APIRouter
from pydantic import BaseModel

from rag.router.query_router import route_query
from rag.chains.graph_query_chain import graph_query
from rag.chains.hybrid_retrieval_chain import hybrid_chain
from rag.chains.recommendation_chain import recommendation_chain

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/")
def query(req: QueryRequest):
    route = route_query(req.question)

    if route == "graph":
        answer = graph_query(req.question)
    elif route == "vector":
        answer = hybrid_chain(req.question)
    else:
        answer = recommendation_chain(req.question)
    return {"answer": answer}