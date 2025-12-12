# Tech Stack Recommendation
- Frontend: React + Vite (TypeScript); state with Zustand/Context; styling via Tailwind or CSS Modules; accessible UI primitives (Radix UI); fetch to FastAPI backend.
- Backend: FastAPI + Pydantic; orchestrate async scraping; REST endpoints for /plan and /health; background queue worker for long scrapes.
- Data sourcing: Playwright (Python) scrapers for Makemytrip, Cleartrip, TripAdvisor + ~20 providers; rotating headers/agents, retries, dedupe, HTML parsing; respect robots/legal and add rate limits.
- Database: PostgreSQL (pgvector enabled) for structured data and embeddings; SQLite acceptable for local dev.
- AI Agent: LangChain or LlamaIndex with GPT-4o/Claude; tools for scraped travel data; embeddings for history/preferences; prompt to ask minimal clarifying questions then synthesize plan/costs.
- DevOps: Docker for local; Ruff + Black + Pytest; Playwright tests for scrapers; simple CI workflow; caching layer (Redis) and task queue (RQ/Celery).
