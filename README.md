
![RAG Tests](https://github.com/hamadliaqat682/ai-rag-chatbot-supabase/actions/workflows/tests.yml/badge.svg)


# AI RAG Chatbot with FastAPI, OpenAI & Supabase

A **runnable educational demo** of a retrieval-augmented generation (RAG)
knowledge assistant. Ingest text, generate embeddings, store searchable chunks
in PostgreSQL/pgvector via Supabase, and answer questions using retrieved
excerpts with source names.

> **Portfolio disclosure:** This is an original demonstration project, not a
> client deployment or an assertion of production readiness. Live endpoints
> require your own OpenAI and Supabase credentials and usage charges may apply.

## Features

- FastAPI endpoints: `/health`, `/ingest`, `/ask`
- Text chunking with overlap and unit tests
- OpenAI `text-embedding-3-small` embeddings (1536 dimensions)
- Supabase PostgreSQL and pgvector semantic similarity retrieval
- Grounded answers with retrieved source filenames
- No live keys or private client data in this repository

## Project layout

```text
app/            FastAPI app and pure chunking utilities
sql/schema.sql  pgvector table and retrieval SQL function
tests/          Offline unit and API validation tests
sample_docs/    Fictional text to ingest
docs/           Architecture and production considerations
.env.example    Placeholder configuration (never commit .env)
```

## Local setup

Requires Python 3.10+ and access to an OpenAI API key and Supabase project.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

1. Run `sql/schema.sql` in the **Supabase SQL Editor**.
2. Copy `.env.example` to `.env`, and fill in the three required credentials.
3. Load `.env` into your process (e.g. `pip install python-dotenv` and `python-dotenv run -- uvicorn app.main:app --reload`) or set shell environment variables directly. The app deliberately does **not** auto-load `.env`.
4. Start: `uvicorn app.main:app --reload`
5. Browse interactive API documentation at `http://127.0.0.1:8000/docs`.

## Example ingestion

```bash
curl -X POST http://127.0.0.1:8000/ingest \
  -H 'Content-Type: application/json' \
  -d '{"source":"example_knowledge.txt","text":"Support hours are Monday through Friday, 9 AM to 5 PM."}'
```

## Ask a question

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"When is support available?"}'
```

The response contains an `answer` and `sources` array. Source attribution
reflects retrieved chunks; always verify important claims against originals.

## Offline tests

```bash
pytest -q
```

The tests validate text chunking, context assembly, the health route, and input validation without requiring credentials.

## Security and deployment notes

- Keep `SUPABASE_SERVICE_ROLE_KEY` **only** on a protected server. Never put it in browser/mobile code or GitHub.
- `/ingest` is unauthenticated in this demo. **Do not expose this API publicly without authentication**, authorization, rate limits, and tenant isolation.
- The database uses RLS and no public client policies; tighten RPC EXECUTE privileges and backend credentials for real deployments.
- The demo deletes and reinserts chunks from the same `source`: this is **not atomic**. Use an idempotent transaction/upsert for production.
- Extracting PDFs, handling failures/retries, observability, and evaluation metrics are future enhancements.

See [architecture](docs/architecture.md).
