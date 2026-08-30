from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import TimestampMixin, UUIDMixin
from app.core.constants import MAX_EMAIL_LENGTH


class OAuthAccount(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "oauth_accounts"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    provider_user_id: Mapped[str] = mapped_column(
        String(MAX_EMAIL_LENGTH),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="oauth_accounts",
    )

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_oauth_provider_user",
        ),
    )
