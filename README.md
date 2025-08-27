# FastAPI Template

A production-ready FastAPI template with modern development tooling, comprehensive testing, and Docker containerization.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Docker** - Containerized development and deployment
- **Poetry** - Dependency management
- **Pytest** - Comprehensive testing with testcontainers
- **Code Quality** - Black (formatter) + Ruff (linter)
- **Database** - PostgreSQL with Alembic migrations
- **Makefile** - Unified development commands

## Quick Start

### 1. Setup Environment

```bash
make setup
```

This creates `.env.dev`, `.env.prod`, and `.env.test` files from `.env.example`.

### 2. Start Development Server

```bash
make up
```

The API will be available at `http://127.0.0.1:50100` (configurable in `.env.dev`).

### 3. Run Tests

```bash
make test
```

Runs unit, database, and end-to-end tests using testcontainers for full isolation.

## API Endpoints

- `GET /` - Hello World
- `GET /health` - Health check

## Development Commands

| Command | Description |
|---------|-------------|
| `make setup` | Initialize environment files |
| `make up` | Start development containers |
| `make down` | Stop development containers |
| `make test` | Run all tests |
| `make unit-test` | Run unit tests only |
| `make db-test` | Run database tests only |
| `make e2e-test` | Run end-to-end tests only |
| `make format` | Format code with Black and fix with Ruff |
| `make lint` | Check code format and lint |
| `make shell` | Open shell in API container |
| `make logs` | View API container logs |

## Project Structure

```
src/
├── api/v1/           # API version 1
├── config/           # Configuration
├── db/               # Database models
├── middlewares/      # Custom middleware
└── main.py          # FastAPI application

tests/
├── unit/            # Unit tests (TestClient)
├── db/              # Database tests (testcontainers)
└── e2e/             # End-to-end tests (testcontainers + HTTP)

alembic/             # Database migrations
```

## Environment Variables

Configure in `.env.dev`, `.env.prod`, and `.env.test`:

- `HOST_BIND_IP` - IP to bind (default: 127.0.0.1)
- `HOST_PORT` - Port to bind (default: 50100)
- `DATABASE_URL` - PostgreSQL connection string

## Testing

The project includes three types of tests:

- **Unit Tests**: Fast tests using FastAPI TestClient
- **Database Tests**: PostgreSQL integration tests using testcontainers
- **E2E Tests**: Full stack tests using Docker Compose via testcontainers

All tests run independently without external dependencies.

## Deployment

### Production

```bash
make up-prod
```

Uses production environment configuration from `.env.prod`.

### Docker Build

The Dockerfile includes multi-stage builds:
- `builder` - Full development environment
- `prod-builder` - Production dependencies only
- `runner` - Minimal production runtime

## Adding Database Models

1. Create models in `src/db/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

Database migrations run automatically in Docker containers.

## Code Quality

- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **Pytest**: Testing framework with testcontainers

Run `make format` and `make lint` before committing.