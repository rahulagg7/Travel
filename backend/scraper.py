"""Scraper scaffolding for travel sites using Playwright (Python).

Each scrape_* function should aggregate results across ~20 sites (config.TOP_SITES).
Current implementation returns sample data; replace with real Playwright flows.
"""
from typing import List, Dict, Any, Callable, Awaitable

from . import config

try:
    from playwright.async_api import async_playwright  # type: ignore
except Exception:  # pragma: no cover - optional dependency at runtime
    async_playwright = None


RouteScraper = Callable[[str, str, str | None], Awaitable[List[Dict[str, Any]]]]
StayScraper = Callable[[str], Awaitable[List[Dict[str, Any]]]]
ActivityScraper = Callable[[str], Awaitable[List[Dict[str, Any]]]]


async def _fetch_with_playwright(url: str, wait_selector: str | None = None) -> str:
    """Fetch a page and return HTML. Replace selectors/flows per site."""
    if not async_playwright:
        return ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(extra_http_headers=config.DEFAULT_HEADERS)
        await page.goto(url, timeout=config.REQUEST_TIMEOUT * 1000)
        if wait_selector:
            await page.wait_for_selector(wait_selector, timeout=config.REQUEST_TIMEOUT * 1000)
        content = await page.content()
        await browser.close()
        return content


async def scrape_routes(origin: str, destination: str, date: str | None = None) -> List[Dict[str, Any]]:
    # TODO: replace with real Playwright flows; this stub returns sample data.
    results: List[Dict[str, Any]] = [
        {"source": "makemytrip", "mode": "flight", "summary": f"{origin}->{destination} morning", "price": 220},
        {"source": "cleartrip", "mode": "train", "summary": f"{origin}->{destination} overnight", "price": 80},
        {"source": "skyscanner", "mode": "flight", "summary": f"{origin}->{destination} evening", "price": 260},
    ]
    return results


async def scrape_accommodations(destination: str) -> List[Dict[str, Any]]:
    # TODO: implement per-site stays scraping with Playwright.
    return [
        {"source": "tripadvisor", "name": "Harborfront Suites", "price": 480, "rating": 4.5},
        {"source": "booking.com", "name": "City Loft", "price": 320, "rating": 4.2},
        {"source": "airbnb", "name": "Old Quarter Loft", "price": 210, "rating": 4.6},
    ]


async def scrape_activities(destination: str) -> List[Dict[str, Any]]:
    # TODO: implement per-site activities scraping.
    return [
        {"source": "tripadvisor", "name": "Old town food walk", "price": 45},
        {"source": "viator", "name": "Sunset cruise", "price": 60},
        {"source": "getyourguide", "name": "Spice plantation tour", "price": 35},
    ]


async def scrape_all(origin: str, destination: str, date: str | None = None) -> Dict[str, Any]:
    # Aggregate helper for background jobs.
    routes = await scrape_routes(origin, destination, date)
    stays = await scrape_accommodations(destination)
    acts = await scrape_activities(destination)
    return {"routes": routes, "stays": stays, "activities": acts}
