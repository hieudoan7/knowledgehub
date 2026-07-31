# KnowledgeHub

> An AI-powered knowledge management platform that enables users to upload documents, search semantically, and interact with their knowledge through natural language.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED)

---

## Overview

KnowledgeHub is a full-stack AI application that allows users to upload documents and ask questions about them using natural language.

Instead of manually searching through PDFs, Word documents, or notes, users can chat with their own knowledge base powered by Retrieval-Augmented Generation (RAG).

The project is built to demonstrate production-ready software engineering practices alongside modern AI technologies.

---

## Features (Planned)

- User authentication (JWT)
- Document upload
  - PDF
  - DOCX
  - TXT
  - Markdown
- Automatic document processing
- Semantic search
- AI-powered question answering
- Source citations
- Chat history
- Background processing
- Dockerized deployment

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- Docker

### Frontend

- React
- TypeScript
- Tailwind CSS

### AI

- OpenAI API
- LangChain (or direct SDKs)
- pgvector
- Sentence Transformers

### DevOps

- Docker Compose
- GitHub Actions

---

## High-Level Architecture

```
                React Frontend
                       │
                REST API (FastAPI)
                       │
      ┌────────────────┼────────────────┐
      │                │                │
 Authentication   Document API     Chat API
      │                │                │
      └────────────────┼────────────────┘
                       │
                 PostgreSQL + pgvector
                       │
                Background Workers
                       │
               Embedding Generation
                       │
                  Large Language Model
```

---

## Project Structure

```
knowledgehub/
│
├── backend/
│
├── frontend/
│
├── docs/
│
├── docker-compose.yml
│
└── README.md
```

---

## Development Roadmap

### Phase 1
- [ ] Project setup
- [ ] Docker environment
- [ ] FastAPI backend
- [ ] React frontend
- [ ] PostgreSQL
- [ ] Authentication

### Phase 2
- [ ] File upload
- [ ] Document parsing
- [ ] Chunking
- [ ] Embedding generation
- [ ] Vector storage

### Phase 3
- [ ] Semantic search
- [ ] Chat API
- [ ] Citation support
- [ ] Conversation history

### Phase 4
- [ ] Background jobs
- [ ] Redis caching
- [ ] Unit tests
- [ ] Integration tests
- [ ] Logging

### Phase 5
- [ ] Deployment
- [ ] CI/CD
- [ ] Documentation
- [ ] Performance optimization

---

## Goals

This project aims to demonstrate:

- Backend software engineering
- REST API design
- AI application development
- Retrieval-Augmented Generation (RAG)
- Database design
- Authentication and authorization
- Docker-based deployment
- Testing
- Clean Architecture
- Production-ready development workflow

---

## Status

🚧 Currently under active development.

The first milestone is setting up the project foundation with FastAPI, React, PostgreSQL, and Docker.

---

## License

MIT


## Migration Flow
# Generate a migration after changing models
uv run alembic revision --autogenerate -m "describe your change"

# Apply the latest migration
uv run alembic upgrade head

# Roll back one migration
uv run alembic downgrade -1

# Show current migration
uv run alembic current

# Show migration history
uv run alembic history

