from sqlalchemy import Boolean, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import TimestampMixin, UUIDMixin
from app.core.constants import MAX_EMAIL_LENGTH, MAX_NAME_LENGTH, MAX_PASSWORD_HASH_LENGTH


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(MAX_EMAIL_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(MAX_PASSWORD_HASH_LENGTH),
        nullable=False,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(MAX_NAME_LENGTH),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan",    
    )
