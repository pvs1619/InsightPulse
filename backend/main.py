import os
import sys
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("insightpulse")

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routes import router

app = FastAPI(
    title="InsightPulse API",
    description="Investment Analysis Using Natural Language Processing & Predictive Analytics",
    version="1.0.0"
)

# Explicitly allowed local development origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://insight-pulse-liard.vercel.app",
]

# Enable CORS for Next.js frontend development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def _get_cors_headers(request: Request) -> dict:
    origin = request.headers.get("origin")
    if origin and (origin in ALLOWED_ORIGINS or "localhost" in origin or "127.0.0.1" in origin):
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        }
    return {}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    headers = _get_cors_headers(request)
    logger.warning(f"HTTP {exc.status_code} on {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        headers=headers,
        content={"detail": exc.detail, "path": request.url.path}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    headers = _get_cors_headers(request)
    logger.error(f"Internal Server Error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        headers=headers,
        content={
            "detail": f"Server Processing Error: {str(exc)}",
            "path": request.url.path
        }
    )

app.include_router(router)

@app.get("/")
def root():
    return {
        "project": "InsightPulse",
        "title": "Investment Analysis Using Natural Language Processing",
        "subtitle": "Financial News Sentiment, Risk and Market Analysis Using NLP and Predictive Analytics",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
