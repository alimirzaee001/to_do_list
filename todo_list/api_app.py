"""
FastAPI application entrypoint for the ToDo List service.
"""

from fastapi import FastAPI

from .api.routes import router as api_router

app = FastAPI(
    title="ToDo List API",
    version="1.0.0",
    description="FastAPI-based web service for managing projects and tasks.",
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
def healthcheck():
    return {"status": "ok"}
