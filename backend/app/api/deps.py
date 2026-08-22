from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.config import settings
from app.storage.base import StorageService
from app.storage.factory import get_storage_service
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.document import DocumentService
from app.exceptions.auth import InvalidTokenError
from app.core.constants import ACCESS_TOKEN_TYPE, SUBJECT_CLAIM, TOKEN_TYPE_CLAIM
from app.services.document_processing import DocumentProcessingService
from app.embeddings.base import EmbeddingService
from app.embeddings.factory import get_embedding_service
from app.services.search import SearchService
from app.llm.base import LLMService
from app.llm.factory import get_llm_service
from app.services.chat import ChatService
from app.repositories.chat_history import ChatHistoryRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
)


def get_user_repository(
    session: Session = Depends(get_db),
) -> UserRepository:
    """Return a UserRepository instance."""
    return UserRepository(session)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Return an AuthService instance."""
    return AuthService(user_repository)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Return the currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        token_type = payload.get(TOKEN_TYPE_CLAIM)
        if token_type != ACCESS_TOKEN_TYPE:
            raise credentials_exception

        subject = payload.get(SUBJECT_CLAIM)

        if subject is None:
            raise credentials_exception

        user_id = UUID(subject)

    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


# Document dependencies
def get_document_repository(
    db: Session = Depends(get_db),
) -> DocumentRepository:
    """Return a document repository instance."""

    return DocumentRepository(db)


# def get_storage_service() -> StorageService:
#     """Return the configured storage service."""

#     return get_storage_service()

def get_document_chunk_repository(
    db: Session = Depends(get_db),
) -> DocumentChunkRepository:
    """Return a document chunk repository."""

    return DocumentChunkRepository(db)

def get_document_processing_service(
    storage_service: StorageService = Depends(get_storage_service),
    document_repository: DocumentRepository = Depends(get_document_repository),
    document_chunk_repository: DocumentChunkRepository = Depends(get_document_chunk_repository,),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
) -> DocumentProcessingService:
    return DocumentProcessingService(
        storage_service=storage_service,
        document_repository=document_repository,
	    document_chunk_repository=document_chunk_repository,
        embedding_service=embedding_service,
    )

def get_document_service(
    db: Session = Depends(get_db),
    document_repository: DocumentRepository = Depends(get_document_repository),
    storage_service: StorageService = Depends(get_storage_service),
) -> DocumentService:
    """Return a document service instance."""

    return DocumentService(
        session=db,
        document_repository=document_repository,
        storage_service=storage_service,
    )

def get_embeddings() -> EmbeddingService:
    return get_embedding_service()

def get_search_service(
    document_chunk_repository: DocumentChunkRepository = Depends(
        get_document_chunk_repository,
    ),
) -> SearchService:
    """Return a search service."""

    embedding_service: EmbeddingService = get_embedding_service()

    return SearchService(
        embedding_service=embedding_service,
        document_chunk_repository=document_chunk_repository,
    )

def get_llm_dependency() -> LLMService:
    """Return the configured LLM service."""

    return get_llm_service()


def get_chat_history_repository(
    session: Session = Depends(get_db),
) -> ChatHistoryRepository:
    """Return a ChatHistoryRepository instance."""

    return ChatHistoryRepository(session)


def get_chat_service(
    session: Session = Depends(get_db),
    search_service: SearchService = Depends(
        get_search_service,
    ),
    llm_service: LLMService = Depends(
        get_llm_dependency,
    ),
    chat_history_repository: ChatHistoryRepository = Depends(
            get_chat_history_repository,
    ),
) -> ChatService:
    """Return a chat service."""

    return ChatService(
        session=session,
        search_service=search_service,
        llm_service=llm_service,
        chat_history_repository=chat_history_repository,
    )
