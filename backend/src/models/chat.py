"""ChatMessage SQLModel entity."""
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class ChatMessage(SQLModel, table=True):
    """ChatMessage entity representing a conversation message."""

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique message identifier"
    )
    user_id: UUID = Field(
        nullable=False,
        index=True,
        description="Owning user identifier (UUID)"
    )
    role: str = Field(
        max_length=20,
        nullable=False,
        description="Message role: 'user' or 'assistant'"
    )
    content: str = Field(
        nullable=False,
        description="Message content"
    )
    message_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Optional metadata (task IDs, operations, etc.)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Creation timestamp"
    )

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role='{self.role}', user_id={self.user_id})>"
