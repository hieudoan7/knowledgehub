# Database Design

## Entities

### User

- id
- email
- password_hash
- created_at

---

### Document

- id
- owner_id
- filename
- status
- created_at

---

### Chunk

- id
- document_id
- content
- embedding

---

### Conversation

- id
- user_id

---

### Message

- id
- conversation_id
- role
- content