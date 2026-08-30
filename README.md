# KnowledgeHub

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A production-ready Retrieval-Augmented Generation (RAG) platform that enables users to upload documents, perform semantic search, and chat with their knowledge using AI.

## 🚀 Live Demo

### [👉 Open KnowledgeHub](https://knowledgehub-taupe.vercel.app/)

Upload your own documents and ask questions using AI-powered semantic search and RAG.

**GitHub:** https://github.com/hieudoan7/knowledgehub

KnowledgeHub is deployed as a full-stack application with a React frontend, FastAPI backend, PostgreSQL + pgvector, background document processing, HTTPS, and CI/CD.

---

## 🎯 How It Works

1. **Upload a document** — Upload a PDF or TXT file.
2. **Process the document** — KnowledgeHub extracts the text, splits it into meaningful chunks, and generates embeddings.
3. **Search your knowledge** — Relevant document chunks are retrieved using vector similarity search.
4. **Ask questions** — The RAG pipeline provides relevant context to the LLM before generating an answer.
5. **View sources** — Responses include the source chunks used to generate the answer.

---

# Table of Contents

- [🚀 Live Demo](#-live-demo)
- [✨ Features](#-features)
- [🎯 How It Works](#-how-it-works)
- [Engineering Highlights](#engineering-highlights)
- [Architecture](#architecture)
- [Production Deployment](#production-deployment)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [License](#license)

---

## ✨ Features

### Implemented

- 🔐 JWT Authentication
- 🔑 Google OAuth authentication
- 📄 Document upload
- 📑 PDF and TXT text extraction
- ⚙️ Background document processing
- ✂️ Sentence-aware text chunking
- 🧠 Embedding generation using AWS Bedrock
- 🔍 Semantic search using PostgreSQL + pgvector
- 💬 Retrieval-Augmented Generation (RAG) chat
- 📚 Source attribution
- 📝 Structured logging
- ⚡ Global exception handling
- 🧪 Integration tests with Pytest
- 🏗 Clean Architecture (Service + Repository pattern)
- 🐳 Docker containerisation
- 🔄 GitHub Actions CI/CD
- ☁️ AWS Lightsail deployment
- 🔒 HTTPS with Caddy

---

# Engineering Highlights

This project was designed to demonstrate modern software engineering and practical AI application development.

Highlights include:

- Clean Architecture with Service and Repository layers
- Dependency Injection throughout the application
- Sentence-aware chunking to improve retrieval quality
- Asynchronous document processing
- Vector similarity search with PostgreSQL (pgvector)
- Configuration-driven design using Pydantic Settings
- Structured logging and centralized exception handling
- JWT and Google OAuth authentication
- End-to-end integration tests
- Docker-based deployment
- GitHub Actions CI/CD
- Production deployment on AWS Lightsail
- HTTPS using Caddy

---

# Architecture

```text
                    React Frontend
                           │
                           ▼
                    FastAPI REST API
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 Authentication     Document Service      Chat Service
                           │                  │
                           ▼                  │
                 Background Processing        │
                           │                  │
                           ▼                  │
                    Text Extraction           │
                           │                  │
                           ▼                  │
                 Sentence-aware Chunking      │
                           │                  │
                           ▼                  │
                     Embeddings               │
                           │                  │
                           ▼                  │
                  PostgreSQL + pgvector ◄─────┘
                           │
                           ▼
                    Semantic Retrieval
                           │
                           ▼
                     Prompt Generation
                           │
                           ▼
                     AWS Bedrock
                           │
                           ▼
                      AI Response
```
---
# Production Deployment

```text
                    Vercel
               React Frontend
                     │
                     ▼
             HTTPS / Internet
                     │
                     ▼
              AWS Lightsail
                     │
              ┌──────┴──────┐
              │    Caddy    │
              │   HTTPS     │
              └──────┬──────┘
                     │
             ┌───────┴───────┐
             │               │
          FastAPI          Worker
             │               │
             └───────┬───────┘
                     │
                     ▼
              PostgreSQL
                + pgvector
```
---
# Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic

## Database

- PostgreSQL
- pgvector

## AI

- AWS Bedrock
- RAG (Retrieval-Augmented Generation)
- Embeddings
- Vector similarity search
- pgvector

## Infrastructure

- Docker
- Docker Compose

## Testing

- Pytest

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/hieudoan7/knowledgehub.git

cd knowledgehub/backend
```

## Create environment file

```bash
cp .env.example .env.local
```

Update the environment variables as required.

---

## Install dependencies

Using uv

```bash
uv sync
```

---

## Run database migrations

```bash
uv run alembic upgrade head
```

---

## Start the application

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at

```
http://localhost:8000
```

Interactive API documentation

```
http://localhost:8000/docs
```

---

# Running Tests

Run all tests

```bash
uv run pytest
```

Run integration tests

```bash
uv run pytest tests/integration
```

---

# License

This project is licensed under the MIT License.