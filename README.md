Travel Recommender AI Agent

Quickstart:
- Frontend: open `index.html` in a browser (static mock UI).
- Backend: `cd backend && uvicorn main:app --reload` (requires Python 3.11+, `pip install -r requirements.txt`).
- Plan endpoint: POST http://localhost:8000/plan with `{ "origin": "DEL", "destination": "GOI", "date": "2025-12-30" }`.
- Health: GET http://localhost:8000/health
- Tests: `cd backend && pytest` (unit tests for agent selection and scraper placeholders)

Notes:
- Scrapers are stubbed; Playwright flows per provider should replace the placeholders. All sites in `config.TOP_SITES` are mapped to placeholder scrapers so aggregation keeps working during development.
- Agent picks the cheapest reasonable transport, a value stay (price with rating nudge), and top activities (de-duped, sorted by price) and returns a total estimate.
