import os
import time
from typing import AsyncGenerator, Generator, Optional

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from alembic import command
from alembic.config import Config
from src.db.database import Base, get_db
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def db_setup(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Generator[str, None, None]:
    """
    Session-scoped fixture to manage the test database container.
    Handles xdist by having the master node create the DB container and share its URL.
    """
    is_master = not hasattr(request.config, "workerinput")

    db_conn_file = None
    if request.config.pluginmanager.is_registered("xdist"):
        root_tmp_dir = tmp_path_factory.getbasetemp().parent
        db_conn_file = root_tmp_dir / "db_url.txt"

    container: Optional[PostgresContainer] = None
    db_url_value: str

    if is_master:
        load_dotenv(".env.test", override=True)
        container = PostgresContainer(
            "postgres:16-alpine",
            driver="psycopg",
            username=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            dbname=os.environ.get("POSTGRES_DB"),
        )
        container.start()
        db_url_value = container.get_connection_url()

        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", db_url_value)
        command.upgrade(alembic_cfg, "head")

        if db_conn_file:
            db_conn_file.write_text(db_url_value)
    else:
        if not db_conn_file:
            pytest.fail("xdist is running but db_conn_file path is missing.")

        timeout = 20
        start_time = time.time()
        while not db_conn_file.exists():
            if time.time() - start_time > timeout:
                pytest.fail(f"Worker timed out waiting for db_url.txt.")
            time.sleep(0.1)
        db_url_value = db_conn_file.read_text()

    yield db_url_value

    if is_master and container:
        container.stop()
        if db_conn_file and db_conn_file.exists():
            db_conn_file.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def db_engine(db_setup: str) -> Generator[Engine, None, None]:
    """Provides a SQLAlchemy engine for the session."""
    engine = create_engine(db_setup)
    yield engine
    engine.dispose()


@pytest.fixture
def db(db_engine: Engine) -> Generator[Session, None, None]:
    """
    Provides a transactional scope for each test function.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    # Clean up all tables before the test runs
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
async def client(db: Session) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides a test client with a transactional database session.
    """
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.pop(get_db, None)
