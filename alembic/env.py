from sqlalchemy import create_engine, pool

from alembic import context
from src.config import db_settings

config = context.config

target_metadata = None


def run_migrations_online() -> None:
    settings = db_settings
    database_url = settings.DATABASE_URL

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    pass  # Offline mode not implemented
else:
    run_migrations_online()
