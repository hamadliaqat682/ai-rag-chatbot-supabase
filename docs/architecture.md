# Architecture

```mermaid
flowchart LR
 A[Document text] --> B[Chunking]
 B --> C[OpenAI embeddings]
 C --> D[(Supabase pgvector)]
 E[User question] --> F[Question embedding]
 F --> G[Similarity search]
 D --> G
 G --> H[Context with source names]
 H --> I[OpenAI answer generation]
 I --> J[Answer and sources]
```

This project is an educational prototype, not a production service.
For production: enforce authentication and per-tenant document isolation; add
upload/format checks, prompt-injection defenses, input limits, observability,
rate limits, retries, transactional upsert, permissions, and careful data retention.
