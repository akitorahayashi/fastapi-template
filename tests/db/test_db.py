import psycopg
from testcontainers.postgres import PostgresContainer


def test_db_connection():
    """Smoke test for PostgreSQL database connection."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        connection_url = postgres.get_connection_url()
        # Convert testcontainers URL format to psycopg format
        psycopg_url = connection_url.replace("postgresql+psycopg2://", "postgresql://")

        with psycopg.connect(psycopg_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                assert result[0] == 1


def test_db_version():
    """Smoke test to check PostgreSQL version."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        connection_url = postgres.get_connection_url()
        # Convert testcontainers URL format to psycopg format
        psycopg_url = connection_url.replace("postgresql+psycopg2://", "postgresql://")

        with psycopg.connect(psycopg_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                assert "PostgreSQL" in version
