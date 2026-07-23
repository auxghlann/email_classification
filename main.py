from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.api.v1 import classifier_router
from app.services.classifier_service import get_classifier_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Warm up / verify model loading on startup
    get_classifier_service()
    yield


app = FastAPI(
    title="Email Classification API",
    description="FastAPI service for classifying emails as spam or not spam using Logistic Regression.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(classifier_router, prefix="/api/v1", tags=["Classification"])


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "Email Classification API"}
