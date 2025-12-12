import asyncio

from backend import config, scraper


def test_placeholder_scrapers_cover_top_sites():
    # All providers listed in config.TOP_SITES should have scrapers populated.
    for name in config.TOP_SITES:
        assert name in scraper.ROUTE_SCRAPERS
        assert name in scraper.STAY_SCRAPERS
        assert name in scraper.ACTIVITY_SCRAPERS


def test_scrape_all_returns_data_with_placeholders():
    data = asyncio.run(scraper.scrape_all("DEL", "BOM", "2025-12-30"))
    assert data["routes"], "Routes should be populated"
    assert data["stays"], "Stays should be populated"
    assert data["activities"], "Activities should be populated"
