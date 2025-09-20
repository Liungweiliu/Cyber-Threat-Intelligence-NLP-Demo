from fastapi import APIRouter

from src.api.schema import QueryRequest, QueryResponse
from src.models.langchain import qa_model

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/api/analysis/sigma/query", response_model=QueryResponse)
async def query_endpoint(input: QueryRequest):
    result = qa_model.invoke(input.query)
    return QueryResponse(query=result.get("query"), answer=result.get("result"))
