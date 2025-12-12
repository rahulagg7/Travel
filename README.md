Travel Recommender AI Agent

Quickstart:
- Frontend: open `index.html` in a browser (static mock UI).
- Backend: `cd backend && uvicorn main:app --reload` (requires Python 3.11+, `pip install -r requirements.txt`).
- Plan endpoint: POST http://localhost:8000/plan with `{ "origin": "DEL", "destination": "GOI", "date": "2025-12-30" }`.
- Health: GET http://localhost:8000/health

Notes:
- Scrapers are stubbed; wire Playwright flows per provider and return structured results.
- Agent chooses best transport/stay and top activities from scraped lists and returns a total estimate.
