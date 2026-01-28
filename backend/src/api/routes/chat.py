"""Chat API endpoints."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from src.models.database import get_session
from src.services.chat_service import ChatService
from src.api.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatResponse,
    ChatHistoryResponse,
)
from src.api.dependencies.auth import get_current_user, TokenUser


router = APIRouter()


def get_chat_service(session: Session = Depends(get_session)) -> ChatService:
    """Dependency to get ChatService instance."""
    return ChatService(session)


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(
    user_id: UUID,
    request: ChatMessageRequest,
    service: ChatService = Depends(get_chat_service),
    current_user: TokenUser = Depends(get_current_user),
):
    """Send a chat message and get AI response.

    Requires authentication. The authenticated user's ID must match
    the user_id in the URL path.
    """
    # Verify user_id matches authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "FORBIDDEN",
                "message": "Cannot access other users' chat",
                "details": {"requested_user_id": str(user_id)},
            },
        )

    result = service.process_message(user_id, request.message)

    # Convert ChatMessage objects to ChatMessageResponse
    messages = [
        ChatMessageResponse.model_validate(msg) for msg in result["messages"]
    ]

    return ChatResponse(
        response=result["response"],
        task_result=result.get("task_result"),
        messages=messages,
    )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    user_id: UUID,
    limit: int = Query(50, ge=1, le=200, description="Maximum messages to return"),
    service: ChatService = Depends(get_chat_service),
    current_user: TokenUser = Depends(get_current_user),
):
    """Get chat history for a user.

    Requires authentication. The authenticated user's ID must match
    the user_id in the URL path.
    """
    # Verify user_id matches authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "FORBIDDEN",
                "message": "Cannot access other users' chat history",
                "details": {"requested_user_id": str(user_id)},
            },
        )

    messages = service.get_history(user_id, limit)
    message_responses = [ChatMessageResponse.model_validate(msg) for msg in messages]

    return ChatHistoryResponse(
        messages=message_responses,
        total=len(message_responses)
    )


@router.delete("/history", status_code=status.HTTP_200_OK)
async def clear_chat_history(
    user_id: UUID,
    service: ChatService = Depends(get_chat_service),
    current_user: TokenUser = Depends(get_current_user),
):
    """Clear all chat history for a user.

    Requires authentication. The authenticated user's ID must match
    the user_id in the URL path.
    """
    # Verify user_id matches authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "FORBIDDEN",
                "message": "Cannot delete other users' chat history",
                "details": {"requested_user_id": str(user_id)},
            },
        )

    count = service.clear_history(user_id)

    return {
        "message": "Chat history cleared successfully",
        "deleted_count": count
    }
