from fastapi import FastAPI

app = FastAPI(
    title="AI Data Analyst",
    description="AI-powered natural language data analysis platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "AI Data Analyst API is running"
    }