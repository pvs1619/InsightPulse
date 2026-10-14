import os
from pathlib import Path
from typing import Optional

# backend directory (e.g., .../backend)
BACKEND_DIR = Path(__file__).resolve().parent.parent
# repository root directory (e.g., .../InsightPulse)
REPO_ROOT = BACKEND_DIR.parent

def get_data_dir() -> Path:
    """
    Dynamically and reliably resolves the data directory across:
    1. Vercel deployment where the project root is backend/ -> backend/data
    2. Local development running from repository root -> backend/data or REPO_ROOT/data
    3. Standalone scripts running from any working directory
    """
    candidates = [
        BACKEND_DIR / "data",
        REPO_ROOT / "data",
        Path.cwd() / "backend" / "data",
        Path.cwd() / "data",
    ]
    for c in candidates:
        if c.is_dir() and (c / "financial_news.csv").exists():
            return c.resolve()

    # Fallback to backend/data
    return (BACKEND_DIR / "data").resolve()

def get_financial_news_path() -> str:
    """Returns absolute path to financial_news.csv."""
    data_dir = get_data_dir()
    csv_file = data_dir / "financial_news.csv"
    return str(csv_file)

def get_sample_articles_path() -> str:
    """Returns absolute path to sample_articles.csv."""
    data_dir = get_data_dir()
    csv_file = data_dir / "sample_articles.csv"
    return str(csv_file)

def get_market_data_dir() -> str:
    """Returns absolute path to market_data directory."""
    data_dir = get_data_dir()
    mkt_dir = data_dir / "market_data"
    return str(mkt_dir)

def resolve_data_path(relative_path: str) -> str:
    """
    Resolves any arbitrary data path (e.g., 'data/financial_news.csv')
    to an existing absolute path.
    """
    clean = relative_path.replace("\\", "/").lstrip("/")
    if clean.startswith("data/"):
        sub = clean[5:]
    else:
        sub = clean

    data_dir = get_data_dir()
    candidate = data_dir / sub
    if candidate.exists():
        return str(candidate.resolve())

    # Check repo root data as well
    repo_candidate = REPO_ROOT / "data" / sub
    if repo_candidate.exists():
        return str(repo_candidate.resolve())

    return str(candidate.resolve())
