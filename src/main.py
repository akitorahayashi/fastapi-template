from fastapi import FastAPI

from src.api.v1.api import api_router

app = FastAPI(
    title="FastAPI Boilerplate",
    version="0.1.0",
    description="A production-ready FastAPI boilerplate with containerization, database integration, and more.",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok"}
