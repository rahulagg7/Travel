"""Scraper scaffolding for travel sites using Playwright (Python).

Each scrape_* function should aggregate results across ~20 sites (config.TOP_SITES).

This module is structured so you can plug in real Playwright flows for each site
incrementally. For now, site-specific scrapers return structured sample data,
but they are wired through a registry so the rest of the app already behaves
as if it were aggregating from multiple providers.
"""
from typing import List, Dict, Any, Callable, Awaitable
import asyncio

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


# --- Site-specific stub scrapers -------------------------------------------------
# These are intentionally lightweight and deterministic. Replace bodies with
# real Playwright-powered flows as you wire up each provider.


async def _routes_makemytrip(origin: str, destination: str, date: str | None) -> List[Dict[str, Any]]:
    return [
        {
            "source": "makemytrip",
            "mode": "flight",
            "summary": f"{origin}->{destination} non‑stop (MakeMyTrip)",
            "price": 220,
        }
    ]


async def _routes_cleartrip(origin: str, destination: str, date: str | None) -> List[Dict[str, Any]]:
    return [
        {
            "source": "cleartrip",
            "mode": "train",
            "summary": f"{origin}->{destination} overnight (Cleartrip)",
            "price": 80,
        }
    ]


async def _routes_skyscanner(origin: str, destination: str, date: str | None) -> List[Dict[str, Any]]:
    return [
        {
            "source": "skyscanner",
            "mode": "flight",
            "summary": f"{origin}->{destination} evening (Skyscanner)",
            "price": 260,
        }
    ]


async def _stays_tripadvisor(destination: str) -> List[Dict[str, Any]]:
    return [
        {
            "source": "tripadvisor",
            "name": "Harborfront Suites",
            "price": 480,
            "rating": 4.5,
        }
    ]


async def _stays_booking(destination: str) -> List[Dict[str, Any]]:
    return [
        {
            "source": "booking.com",
            "name": "City Loft",
            "price": 320,
            "rating": 4.2,
        }
    ]


async def _stays_airbnb(destination: str) -> List[Dict[str, Any]]:
    return [
        {
            "source": "airbnb",
            "name": "Old Quarter Loft",
            "price": 210,
            "rating": 4.6,
        }
    ]


async def _activities_tripadvisor(destination: str) -> List[Dict[str, Any]]:
    return [
        {"source": "tripadvisor", "name": "Old town food walk", "price": 45},
    ]


async def _activities_viator(destination: str) -> List[Dict[str, Any]]:
    return [
        {"source": "viator", "name": "Sunset cruise", "price": 60},
    ]


async def _activities_getyourguide(destination: str) -> List[Dict[str, Any]]:
    return [
        {"source": "getyourguide", "name": "Spice plantation tour", "price": 35},
    ]


# Registry maps a subset of config.TOP_SITES to concrete scrapers.
ROUTE_SCRAPERS: Dict[str, RouteScraper] = {
    "makemytrip": _routes_makemytrip,
    "cleartrip": _routes_cleartrip,
    "skyscanner": _routes_skyscanner,
}

STAY_SCRAPERS: Dict[str, StayScraper] = {
    "tripadvisor": _stays_tripadvisor,
    "booking": _stays_booking,
    "airbnb": _stays_airbnb,
}

ACTIVITY_SCRAPERS: Dict[str, ActivityScraper] = {
    "tripadvisor": _activities_tripadvisor,
    "viator": _activities_viator,
    "getyourguide": _activities_getyourguide,
}


async def _gather_with_concurrency(
    limit: int, coros: List[Awaitable[List[Dict[str, Any]]]]
) -> List[Dict[str, Any]]:
    """Run a list of coroutines with a simple concurrency limit and flatten results."""
    semaphore = asyncio.Semaphore(limit)
    results: List[Dict[str, Any]] = []

    async def _run(coro: Awaitable[List[Dict[str, Any]]]) -> None:
        async with semaphore:
            try:
                data = await coro
                results.extend(data)
            except Exception:
                # In early versions we fail soft per‑site and keep the rest.
                return

    await asyncio.gather(*[_run(c) for c in coros])
    return results


async def scrape_routes(origin: str, destination: str, date: str | None = None) -> List[Dict[str, Any]]:
    """Aggregate route options from available route scrapers.

    This respects config.MAX_CONCURRENCY and can later be extended to use the
    full config.TOP_SITES list as more providers are implemented.
    """
    active_scrapers = [
        ROUTE_SCRAPERS[name]
        for name in config.TOP_SITES
        if name in ROUTE_SCRAPERS
    ]
    if not active_scrapers:
        return []
    coros = [scraper(origin, destination, date) for scraper in active_scrapers]
    return await _gather_with_concurrency(config.MAX_CONCURRENCY, coros)


async def scrape_accommodations(destination: str) -> List[Dict[str, Any]]:
    """Aggregate accommodation options from available stay scrapers."""
    active_scrapers = [
        STAY_SCRAPERS[name]
        for name in config.TOP_SITES
        if name in STAY_SCRAPERS
    ]
    if not active_scrapers:
        return []
    coros = [scraper(destination) for scraper in active_scrapers]
    return await _gather_with_concurrency(config.MAX_CONCURRENCY, coros)


async def scrape_activities(destination: str) -> List[Dict[str, Any]]:
    """Aggregate activities from available activity scrapers."""
    active_scrapers = [
        ACTIVITY_SCRAPERS[name]
        for name in config.TOP_SITES
        if name in ACTIVITY_SCRAPERS
    ]
    if not active_scrapers:
        return []
    coros = [scraper(destination) for scraper in active_scrapers]
    return await _gather_with_concurrency(config.MAX_CONCURRENCY, coros)


async def scrape_all(origin: str, destination: str, date: str | None = None) -> Dict[str, Any]:
    """Aggregate routes, stays, and activities for use in background jobs."""
    routes = await scrape_routes(origin, destination, date)
    stays = await scrape_accommodations(destination)
    acts = await scrape_activities(destination)
    return {"routes": routes, "stays": stays, "activities": acts}
