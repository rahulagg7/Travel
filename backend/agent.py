"""Agent stub to combine scraped data and choose recommendations."""
from typing import List, Dict, Any


def choose_best_route(routes: List[Dict[str, Any]]) -> Dict[str, Any]:
    return sorted(routes, key=lambda r: r.get("price") or 0)[0] if routes else {}


def choose_best_accommodation(stays: List[Dict[str, Any]]) -> Dict[str, Any]:
    return sorted(stays, key=lambda s: s.get("price") or 0)[0] if stays else {}


def choose_top_activities(activities: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    return activities[:limit]
