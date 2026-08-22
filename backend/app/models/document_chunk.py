from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.db.base_class import Base
from app.db.mixins import TimestampMixin


class DocumentChunk(Base, TimestampMixin):
    """Represents a chunk of a document."""

    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(512),
        nullable=True,
    )

    document = relationship(
        "Document",
        back_populates="chunks",
    )

