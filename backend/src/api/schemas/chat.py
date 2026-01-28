"""Chat Pydantic schemas for API request/response."""
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID


class ChatMessageRequest(BaseModel):
    """Schema for sending a chat message."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User message (required, 1-2000 characters)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Create a task to buy groceries"
            }
        }
    )


class ChatMessageResponse(BaseModel):
    """Schema for a single chat message."""

    id: UUID = Field(..., description="Unique message identifier")
    user_id: UUID = Field(..., description="Owning user identifier")
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    message_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "550e8400-e29b-41d4-a716-446655440001",
                "role": "user",
                "content": "Create a task to buy groceries",
                "message_metadata": None,
                "created_at": "2026-01-28T10:30:00Z"
            }
        }
    )


class ChatResponse(BaseModel):
    """Schema for chat API response."""

    response: str = Field(..., description="Assistant's response message")
    task_result: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Task operation result if applicable"
    )
    messages: List[ChatMessageResponse] = Field(
        ...,
        description="Updated conversation history"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "I've created a new task: 'Buy groceries'",
                "task_result": {
                    "id": "550e8400-e29b-41d4-a716-446655440002",
                    "title": "Buy groceries",
                    "is_completed": False
                },
                "messages": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "user_id": "550e8400-e29b-41d4-a716-446655440001",
                        "role": "user",
                        "content": "Create a task to buy groceries",
                        "message_metadata": None,
                        "created_at": "2026-01-28T10:30:00Z"
                    }
                ]
            }
        }
    )


class ChatHistoryResponse(BaseModel):
    """Schema for chat history response."""

    messages: List[ChatMessageResponse] = Field(..., description="List of messages")
    total: int = Field(..., description="Total number of messages")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "user_id": "550e8400-e29b-41d4-a716-446655440001",
                        "role": "user",
                        "content": "Show me all my tasks",
                        "message_metadata": None,
                        "created_at": "2026-01-28T10:30:00Z"
                    }
                ],
                "total": 1
            }
        }
    )
