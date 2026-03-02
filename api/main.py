from fastapi import FastAPI
from pydantic import BaseModel
from retrieval.retriever import retrieve

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(request: QueryRequest):
    results = retrieve(request.query, top_k=10)

    formatted = []
    for r in results:
        formatted.append({
            "url": r["url"],
            "name": r["name"],
            "adaptive_support": "Yes",
            "description": r["description"],
            "duration": 30,
            "remote_support": "Yes",
            "test_type": ["Knowledge & Skills"]
        })

    return {"recommended_assessments": formatted}