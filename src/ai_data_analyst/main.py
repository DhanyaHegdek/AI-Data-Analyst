from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai_data_analyst.agents.graph import analyst_graph
from ai_data_analyst.services.query_history import (
    get_query_history,
    save_query,
)


app = FastAPI(
    title="AI Data Analyst",
    description="AI-powered natural language data analysis platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mm
class AnalyzeRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "AI Data Analyst API is running",
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = analyst_graph.invoke(
        {
            "question": request.question,
        }
    )

    # Save only successful analyses
    if not result.get("error"):
        save_query(
            question=request.question,
            generated_sql=result.get("sql"),
        )

    return {
        "question": result.get("question"),
        "sql": result.get("sql"),
        "is_valid": result.get("is_valid"),
        "retry_count": result.get("retry_count", 0),
        "rows": result.get("rows"),
        "analysis": result.get("analysis"),
        "visualization": result.get("visualization"),
        "final_response": result.get("final_response"),
        "error": result.get("error"),
    }


@app.get("/history")
def history():
    queries = get_query_history(limit=50)

    return [
        {
            "id": query.id,
            "question": query.question,
            "generated_sql": query.generated_sql,
            "created_at": query.created_at.isoformat(),
        }
        for query in queries
    ]