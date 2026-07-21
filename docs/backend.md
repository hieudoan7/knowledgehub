# Backend Architecture

## Layers

```
API

↓

Service Layer

↓

Database Layer

↓

Infrastructure
```

---

## Folder Structure

```
app/

├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── workers/
├── tests/
└── main.py
```

---

## Responsibilities

### API

HTTP endpoints only.

### Services

Business logic.

### Models

Database entities.

### Schemas

Validation and serialization.

### Core

Configuration, security and shared utilities.

### Workers

Background processing.

### Tests

Unit and integration tests.