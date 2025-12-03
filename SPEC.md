# Tech Stack Recommendation
- Frontend: React + Vite (TypeScript), lightweight state with Zustand/Context, styling via Tailwind CSS or CSS Modules, optional UI primitives (Radix UI) for accessibility.
- Backend: Python (FastAPI) with Pydantic validation, async scraping/orchestration endpoints; caching via Redis; task queue (Celery/RQ) for scraper jobs.
- Data sources: Scrape Makemytrip, Cleartrip, TripAdvisor and ~20 total travel/activity sites via Playwright/Puppeteer/Playwright-Python with rotating user agents and optional proxies; respect robots/legal; add rate limiting, retries, dedupe, and HTML parsers.
- Database: PostgreSQL (self-hosted or Supabase) with SQLModel/SQLAlchemy; consider SQLite for local/offline runs.
- AI Agent: LangChain or LlamaIndex orchestrating GPT-4o/Claude models, embeddings store (Postgres pgvector or Chroma) for past trips/prompts, tool-calling for scraped travel data; agent should ask minimal clarifying questions and synthesize accommodation/transport/activities/costs.
- DevOps: Docker for local runs, Pytest for units, Playwright tests for scraping, CI lint/format with Ruff + Black.
