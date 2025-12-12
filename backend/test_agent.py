from backend import agent


def test_choose_best_route_prefers_lower_price_then_mode():
    routes = [
        {"mode": "bus", "price": 50},
        {"mode": "train", "price": 50},
        {"mode": "flight", "price": 80},
    ]
    best = agent.choose_best_route(routes)
    assert best["mode"] == "train"  # same price, better mode ranking than bus


def test_choose_best_accommodation_values_rating():
    stays = [
        {"name": "Cheap but low rating", "price": 120, "rating": 2.5},
        {"name": "Slightly pricier, better rating", "price": 140, "rating": 4.5},
    ]
    best = agent.choose_best_accommodation(stays)
    assert best["name"] == "Slightly pricier, better rating"


def test_choose_top_activities_dedupes_and_sorts():
    acts = [
        {"name": "Food tour", "price": 60},
        {"name": "food tour", "price": 55},  # duplicate name different case
        {"name": "Sunset cruise", "price": 70},
        {"name": "Museum", "price": 40},
    ]
    picked = agent.choose_top_activities(acts, limit=3)
    names = [a["name"] for a in picked]
    assert "Food tour" in names or "food tour" in names
    assert len(picked) == 3
    assert names[0] == "Museum"  # lowest price first
