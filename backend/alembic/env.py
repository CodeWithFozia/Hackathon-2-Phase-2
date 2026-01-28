"""Alembic environment configuration."""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
from src.config import settings
from src.models.task import Task  # Import all models
from src.models.user import User  # Import user model for auth
from src.models.chat import ChatMessage  # Import chat model

# Interpret the config file for Python logging.
fileConfig("alembic.ini")

# Set target metadata for autogenerate support
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Use database URL from settings instead of alembic.ini
    # Determine connect_args based on database type
    connect_args = {}
    if settings.database_url.startswith("postgresql"):
        connect_args = {"ssl": "require"}

    connectable = create_engine(
        settings.database_url,
        poolclass=pool.NullPool,
        connect_args=connect_args
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
