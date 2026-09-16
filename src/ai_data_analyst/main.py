from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ai_data_analyst.agents.graph import analyst_graph


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