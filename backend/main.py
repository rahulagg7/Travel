from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

from . import scraper, agent  # type: ignore

app = FastAPI(title="Travel Planner Agent", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JourneyRequest(BaseModel):
    origin: str = Field(..., description="Start city/airport")
    destination: str = Field(..., description="Destination city/airport")
    date: Optional[str] = Field(None, description="Preferred departure date (YYYY-MM-DD)")
    notes: Optional[str] = Field(None, description="Preferences/constraints")

class Activity(BaseModel):
    name: str
    price: Optional[float] = None
    source: Optional[str] = None

class Recommendation(BaseModel):
    accommodation: str
    accommodation_price: Optional[float] = None
    transport: str
    transport_price: Optional[float] = None
    activities: List[Activity] = Field(default_factory=list)
    total_estimate: Optional[float] = None
    sources_used: List[str] = Field(default_factory=list)

@app.post("/plan", response_model=Recommendation)
async def plan_trip(payload: JourneyRequest) -> Recommendation:
    """Stub endpoint: scrape ~20 sites, rank options, return picks."""
    routes = await scraper.scrape_routes(payload.origin, payload.destination, payload.date)
    stays = await scraper.scrape_accommodations(payload.destination)
    acts_raw = await scraper.scrape_activities(payload.destination)

    best_route = agent.choose_best_route(routes)
    best_stay = agent.choose_best_accommodation(stays)
    top_acts = agent.choose_top_activities(acts_raw)

    activities = [Activity(name=a.get("name", "Activity"), price=a.get("price"), source=a.get("source")) for a in top_acts]
    total = (best_route.get("price") or 0) + (best_stay.get("price") or 0) + sum(a.price or 0 for a in activities)
    sources = list({item.get("source") for item in routes + stays + acts_raw if item.get("source")})

    return Recommendation(
        accommodation=best_stay.get("name", "Accommodation TBD"),
        accommodation_price=best_stay.get("price"),
        transport=f"{best_route.get('mode', 'transport')} {payload.origin} -> {payload.destination}",
        transport_price=best_route.get("price"),
        activities=activities,
        total_estimate=total if total > 0 else None,
        sources_used=sources,
    )

@app.get("/health")
async def health():
    return {"status": "ok"}
