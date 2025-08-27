# Production-Ready FastAPI Boilerplate

## Overview

This project provides a comprehensive, production-ready boilerplate for building modern web APIs with FastAPI. It comes pre-configured with a suite of powerful tools to handle containerization, database integration, dependency management, and code quality, allowing you to focus on writing business logic instead of setting up infrastructure.

The architecture is designed to be clean, scalable, and easy to extend, making it an ideal starting point for any new FastAPI project.

## Features

-   **Modern Tech Stack**: FastAPI, Python 3.12, and PostgreSQL.
-   **Containerized Environment**: Fully containerized with Docker and Docker Compose for consistent development, testing, and production environments.
-   **Database Integration**: Pre-configured with SQLAlchemy for the ORM and Alembic for handling database migrations.
-   **Dependency Management**: Uses Poetry for robust and reproducible dependency management.
-   **Code Quality**: Integrated with Ruff (linter) and Black (formatter) to ensure clean and consistent code.
-   **Testing Framework**: Includes a full testing suite with Pytest, with support for unit, database-dependent, and end-to-end tests.
-   **Sample CRUD API**: Comes with a sample `/items` CRUD API to demonstrate project structure and best practices.
-   **CI/CD Ready**: Includes GitHub Actions workflows for linting, testing, and building Docker images.

## Setup and Usage

### Prerequisites

-   Docker and Docker Compose
-   `make` command
-   Python & Poetry (for local development without Docker)

### 1. Initialize Your Environment

This command sets up your local environment by creating `.env` files for development, production, and testing from the `.env.example` template. It only needs to be run once.

```sh
make setup
```

### 2. Start the Services

Start the API server and PostgreSQL database for local development.

```sh
make up
```

The API will be accessible at `http://127.0.0.1:8000` by default. The source code is mounted as a volume, enabling hot-reloading on code changes.

### 3. Run Database Migrations

After making changes to your SQLAlchemy models, you need to create a new migration script and apply it.

**Create a new migration:**

```sh
# Open a shell in the running 'api' container
make shell

# Inside the container, run alembic
alembic revision --autogenerate -m "Your migration message"
exit
```

**Apply the migration:**

```sh
make migrate
```

## Project Structure

```
├── alembic/              # Database migration scripts
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py        # Aggregates all v1 routers
│   │       ├── routers/    # API endpoint definitions
│   │       ├── schemas/    # Pydantic schemas
│   │       └── services/   # Business logic
│   ├── config/             # Application settings
│   ├── db/
│   │   ├── database.py   # Database session management
│   │   └── models/       # SQLAlchemy models
│   └── main.py             # FastAPI application entrypoint
├── tests/
│   ├── db/                 # Database-dependent tests
│   ├── e2e/                # End-to-end tests
│   └── unit/               # Unit tests (no external dependencies)
├── .env.example          # Template for environment variables
├── docker-compose.yml    # Docker services definition
├── Dockerfile            # Docker image definition for the API
├── Makefile              # Automation commands
└── pyproject.toml        # Project metadata and dependencies (Poetry)
```

## Development Workflow

A `Makefile` is provided to streamline common development tasks.

| Command         | Description                                                          |
|-----------------|----------------------------------------------------------------------|
| `make help`     | ✨ Shows a help message with all available commands.                 |
| `make setup`    | 🚀 Initializes environment files from `.env.example`.                |
| `make up`       | 🐳 Starts all development containers.                                |
| `make down`     | 🛑 Stops and removes all development containers.                     |
| `make logs`     | 📜 Tails the logs of the API service.                                |
| `make shell`    | 💻 Opens an interactive shell inside the API container.              |
| `make migrate`  | 🗄️ Runs database migrations.                                        |
| `make format`   | 🎨 Formats the codebase using Black.                                 |
| `make lint`     | 🔎 Lints and fixes the code with Ruff.                               |
| `make test`     | 🧪 Runs the full test suite (unit, db, and e2e).                     |
| `make clean`    | 🧹 **Destructive.** Removes containers, networks, and volumes.        |
| `make rebuild`  | 🔄 Rebuilds the API Docker image without cache and restarts it.       |