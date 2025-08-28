# FastAPI Template

A production-ready FastAPI template designed with robust best practices for environment management and developer experience, inspired by the `olm-api` project.

## Core Philosophy

This template enforces a strict separation of configuration between environments, ensuring consistency and simplifying the development workflow. It leverages `docker-compose.override.yml` for development-specific settings and symbolic links for clean environment switching.

## Features

- **FastAPI**: High-performance Python web framework.
- **Docker & Docker Compose**: Containerized development and production parity.
- **Symbolic Link Env Management**: Clean, automated switching between `.env.dev`, `.env.test`, and `.env.prod`.
- **Poetry**: Modern Python dependency management.
- **Pytest**: Comprehensive testing suite.
- **Alembic**: Database schema migrations.
- **Code Quality**: Pre-configured with `black` and `ruff`.
- **CI/CD**: GitHub Actions workflow ready for testing.

## Quick Start

### 1. Initial Setup

First, clone the repository. Then, run the setup command:

```bash
make setup
```

This command performs the following actions:
- Installs Python dependencies using Poetry.
- Creates `.env.dev`, `.env.prod`, and `.env.test` from `.env.example` if they don't exist.

### 2. Start the Development Server

To start the services, run:

```bash
make up
```

This command will:
1.  Create a symbolic link from `.env.dev` to `.env`.
2.  Start the `api` and `db` services using `docker-compose.yml` and `docker-compose.override.yml`.

The API will be available at `http://127.0.0.1:50000` (configurable in `.env.dev`). The `docker-compose.override.yml` keeps the container running with `tail -f /dev/null`, allowing you to attach a shell and run commands manually.

### 3. Running Tests

To run the full test suite:

```bash
make test
```

This command uses `.env.test` to configure the testing environment.

## Environment Variable Management

This project uses a symbolic link (`.env`) to manage environment-specific configurations.

- **`.env.example`**: A template for production environment variables. **Do not** add development or test-specific variables here.
- **`.env.prod`**: Production configuration. Created from `.env.example` on `make setup`.
- **`.env.dev`**: Development configuration. Created from `.env.example` on `make setup`. You should customize this file for your local setup.
- **`.env.test`**: Testing configuration. Created from `.env.example` on `make setup`.

The `make` commands (e.g., `make up`, `make test`) automatically create a symlink from the appropriate file (e.g., `.env.dev`) to `.env`. Docker Compose then automatically picks up the `.env` file. This approach avoids duplicating variables and keeps the environment configuration clean and explicit.

## Development Workflow

| Command | Description | .env Used |
|---------------|--------------------------------------------------|-----------|
| `make setup` | Initialize the project and create `.env.*` files. | N/A |
| `make up` | Start development containers. | `.env.dev`|
| `make down` | Stop development containers. | `.env.dev`|
| `make logs` | View logs for the development API service. | `.env.dev`|
| `make shell` | Open a shell in the running API container. | `.env.dev`|
| `make migrate` | Run database migrations. | `.env.dev`|
| `make test` | Run the complete test suite. | `.env.test`|
| `make up-prod` | Start production-like containers. | `.env.prod`|
| `make down-prod`| Stop production-like containers. | `.env.prod`|
| `make format` | Format code with Black and Ruff. | N/A |
| `make lint` | Lint code with Black and Ruff. | N/A |

## CI/CD Pipeline

The `.github/workflows/run-tests.yml` workflow automatically runs the test suite on every push and pull request to the `main` branch. It uses default values for environment variables, ensuring that tests can run in forked repositories where secrets are not available.