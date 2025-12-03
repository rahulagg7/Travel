"""Scraper stubs for travel sites using Playwright (Python).

Replace the stub functions with real Playwright async scrapers per site.
"""
from typing import List, Dict, Any, Callable

from . import config


# Registry of per-site handlers; each returns a list of result dicts.
RouteScraper = Callable[[str, str, str | None], Any]
StayScraper = Callable[[str], Any]
ActivityScraper = Callable[[str], Any]


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
