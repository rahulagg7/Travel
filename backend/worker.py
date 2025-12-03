"""Background worker stub for scraping via Celery or RQ."""
from typing import Dict, Any

from .scraper import scrape_all

try:
    from rq import Queue
    from redis import Redis
    redis_conn = Redis(host="localhost", port=6379, db=0)
    q = Queue("scrape", connection=redis_conn)
except Exception:  # pragma: no cover - placeholder
    q = None


def enqueue_scrape(origin: str, destination: str, date: str | None = None) -> str:
    """Enqueue a scrape job and return job id."""
    if not q:
        return "local-stub"
    job = q.enqueue(scrape_all, origin, destination, date)
    return job.id


def run_scrape_sync(origin: str, destination: str, date: str | None = None) -> Dict[str, Any]:
    """Synchronous helper for dev/testing."""
    # In production prefer enqueue_scrape and poll for result
    import asyncio
    return asyncio.get_event_loop().run_until_complete(scrape_all(origin, destination, date))
