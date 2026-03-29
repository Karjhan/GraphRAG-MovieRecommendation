from fastapi import APIRouter
from pydantic import BaseModel

from rag.chains.vector_only_chain import vector_only_chain

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/")
def vector_query(req: QueryRequest):
    answer = vector_only_chain(req.question)
    return {"answer": answer}