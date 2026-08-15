from app.db.base_class import Base

# Import all ORM models here so SQLAlchemy registers them
from app.models.user import User  # noqa: F401
from app.models.document import Document  # noqa: F401
from app.models.chat_message_record import ChatMessageRecord  # noqa: F401

