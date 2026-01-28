"""Create chat_messages table migration.

Revision ID: 005
Revises: 004
Create Date: 2026-01-28
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from uuid import uuid4

# revision identifiers
revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create chat_messages table for storing conversation history."""
    op.create_table(
        "chatmessage",
        sa.Column("id", sa.UUID(), nullable=False, default=uuid4),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("message_metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint("id", name="pk_chatmessage"),
    )
    op.create_index("ix_chatmessage_user_id", "chatmessage", ["user_id"], unique=False)
    op.create_index("ix_chatmessage_created_at", "chatmessage", ["created_at"], unique=False)


def downgrade() -> None:
    """Drop chat_messages table."""
    op.drop_index("ix_chatmessage_created_at", table_name="chatmessage")
    op.drop_index("ix_chatmessage_user_id", table_name="chatmessage")
    op.drop_table("chatmessage")
