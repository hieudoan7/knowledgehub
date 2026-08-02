from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, BackgroundTasks

from app.api.deps import (
    get_current_user,
    get_document_service,
    get_search_service,
    get_chat_service,
)
from app.exceptions.document import (
    FileTooLargeError,
    UnsupportedFileTypeError,
)
from app.models.user import User
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentStatusResponse,
)
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
)
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.document import DocumentService
from app.services.search import SearchService
from app.services.chat import ChatService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:
    """Upload a document."""

    try:
        document = document_service.upload(
            owner_id=current_user.id,
            original_filename=file.filename or "unknown",
            mime_type=file.content_type or "",
            content=await file.read(),
            background_tasks=background_tasks,
        )

    except UnsupportedFileTypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type.",
        )

    except FileTooLargeError:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds maximum allowed size.",
        )

    return DocumentResponse.model_validate(document)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    request: DocumentCreate,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:
    """Create a new document."""

    document = document_service.create(
        request=request,
        owner_id=current_user.id,
    )

    return DocumentResponse.model_validate(document)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
) -> list[DocumentResponse]:
    """List all documents belonging to the current user."""

    documents = document_service.list_by_owner(current_user.id)

    return [
        DocumentResponse.model_validate(document)
        for document in documents
    ]


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:
    """Retrieve a document owned by the current user."""

    document = document_service.get_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return DocumentResponse.model_validate(document)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
) -> None:
    """Delete a document owned by the current user."""

    document = document_service.get_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    document_service.delete(document)


@router.post(
    "/{document_id}/process",
    response_model=DocumentResponse,
)
def process_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentResponse:
    """Process an uploaded document."""

    document = document_service.get_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    document = document_service.process_document(document)

    return DocumentResponse.model_validate(document)

@router.post(
    "/{document_id}/search",
    response_model=list[SearchResponse],
)
def search_document(
    document_id: UUID,
    request: SearchRequest,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
    search_service: SearchService = Depends(get_search_service),
) -> list[SearchResponse]:
    """
    Perform semantic search within a document.
    """

    document = document_service.get_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    results = search_service.search(
        document_id=document.id,
        query=request.query,
        limit=request.limit,
    )

    return [
        SearchResponse(
            chunk_index=result.chunk.chunk_index,
            content=result.chunk.content,
            score=result.score,
        )
        for result in results
    ]

@router.post(
    "/{document_id}/chat",
    response_model=ChatResponse,
)
def chat_document(
    document_id: UUID,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """
    Answer questions about a document.
    """

    document = document_service.get_user_document(
        document_id=document_id,
        owner_id=current_user.id,
    )

    return chat_service.chat(
        document_id=document.id,
        question=request.question,
    )

@router.get(
    "/{document_id}/status",
    response_model=DocumentStatusResponse,
)
def get_document_status(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service),
):
    document = document_service.get_status(
        document_id=document_id,
        owner_id=current_user.id,
    )

    return DocumentStatusResponse(
        id=document.id,
        status=document.status,
    )
