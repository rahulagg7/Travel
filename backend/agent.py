"""Agent utilities to pick top transport, stays, and activities from scraped data."""
from typing import List, Dict, Any

_MODE_PREFERENCE = {"flight": 0, "train": 1, "bus": 2, "mixed": 3}


def _price_value(item: Dict[str, Any]) -> float:
    price = item.get("price")
    try:
        return float(price)
    except Exception:
        return float("inf")


def choose_best_route(routes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Pick the cheapest reasonable route, preferring faster modes when prices tie."""
    if not routes:
        return {}
    return sorted(
        routes,
        key=lambda r: (_price_value(r), _MODE_PREFERENCE.get(r.get("mode", ""), 9)),
    )[0]


def choose_best_accommodation(stays: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Pick the value stay: lower price with a nudge toward higher rating."""
    if not stays:
        return {}

    def score(stay: Dict[str, Any]) -> float:
        price = _price_value(stay)
        rating = stay.get("rating") or 0
        # Lower score is better; reward rating meaningfully.
        return price - (rating * 15)

    return sorted(stays, key=score)[0]


def choose_top_activities(activities: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    """Return a de-duplicated, price-sorted list of activities."""
    if not activities:
        return []
    seen = set()
    deduped: List[Dict[str, Any]] = []
    for act in activities:
        key = (act.get("name") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(act)
    deduped.sort(key=_price_value)
    return deduped[:limit]
