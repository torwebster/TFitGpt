# TFit Monorepo

Production-ready starter for TFit (AI Fitness OS) with:
- Next.js web app (`apps/web`)
- FastAPI backend (`apps/api`)
- Postgres + Redis via Docker Compose

## Quick start

```bash
docker compose up --build
```

Web: http://localhost:3000  
API docs: http://localhost:8000/docs

## Local checks

```bash
cd apps/api && pytest
```

## Vertical slice included
- Auth scaffolding (NextAuth Google provider placeholders)
- Onboarding/profile capture
- Adaptive engine deterministic plan generation
- Today plan API + storage
- In-app coach message ingestion/classification/extraction
- Memory writes and auditable message ingest records
- Slack/Discord webhook endpoints (dedupe + bot loop guards)
