# ==============================================================================
# Makefile for Project Automation
#
# Provides a unified interface for common development tasks, abstracting away
# the underlying Docker Compose commands for a better Developer Experience (DX).
#
# Inspired by the self-documenting Makefile pattern.
# See: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# ==============================================================================

# Default target executed when 'make' is run without arguments
.DEFAULT_GOAL := help

# ==============================================================================
# Sudo Configuration
#
# Allows running Docker commands with sudo when needed (e.g., in CI environments).
# Usage: make up SUDO=true
# ==============================================================================
SUDO_PREFIX :=
ifeq ($(SUDO),true)
	SUDO_PREFIX := sudo
endif

DOCKER_CMD := $(SUDO_PREFIX) docker

# Load environment variables from .env file
-include .env

# Define the project name from environment variable
PROJECT_NAME ?= fastapi-tmpl

# Define project names for different environments
DEV_PROJECT_NAME := $(PROJECT_NAME)-dev
PROD_PROJECT_NAME := $(PROJECT_NAME)-prod
TEST_PROJECT_NAME := $(PROJECT_NAME)-test

# Compose command aliases
DEV_COMPOSE := $(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.dev.override.yml --project-name $(DEV_PROJECT_NAME)
PROD_COMPOSE := $(DOCKER_CMD) compose -f docker-compose.yml --project-name $(PROD_PROJECT_NAME)
TEST_COMPOSE := $(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.test.override.yml --project-name $(TEST_PROJECT_NAME)

# ==============================================================================
# HELP
# ==============================================================================

.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target] [VAR=value]"
	@echo "Options:"
	@echo "  \033[36m%-15s\033[0m %s" "SUDO=true" "Run docker commands with sudo (e.g., make up SUDO=true)"
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ==============================================================================
# Environment Setup
# ==============================================================================

.PHONY: setup
setup: ## Initialize project: install dependencies, create .env file and pull required Docker images.
	@echo "Installing python dependencies with uv..."
	@uv sync
	@echo "Creating environment file..."
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..." ; \
		cp .env.example .env; \
	else \
		echo ".env already exists. Skipping creation."; \
	fi
	@echo "✅ Environment file created (.env)"
	@echo "💡 You can customize .env for your specific needs:"
	@echo "   📝 Change OLLAMA_HOST to switch between container/host Ollama"
	@echo "   📝 Adjust other settings as needed"
	@echo ""
	@echo "Pulling PostgreSQL image for tests..."
	$(DOCKER_CMD) pull postgres:16-alpine

# ==============================================================================
# Development Environment Commands
# ==============================================================================

.PHONY: up
up: ## Start all development containers in detached mode
	@echo "Starting up development services..."
	$(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.dev.override.yml --project-name $(DEV_PROJECT_NAME) up -d

.PHONY: down
down: ## Stop and remove all development containers
	@echo "Shutting down development services..."
	$(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.dev.override.yml --project-name $(DEV_PROJECT_NAME) down --remove-orphans

.PHONY: up-prod
up-prod: ## Start all production-like containers
	@echo "Starting up production-like services..."
	$(DOCKER_CMD) compose -f docker-compose.yml --project-name $(PROD_PROJECT_NAME) up -d --build --pull always --remove-orphans

.PHONY: down-prod
down-prod: ## Stop and remove all production-like containers
	@echo "Shutting down production-like services..."
	$(DOCKER_CMD) compose -f docker-compose.yml --project-name $(PROD_PROJECT_NAME) down --remove-orphans
	
.PHONY: rebuild
rebuild: ## Rebuild and restart API container only
	@echo "Rebuilding and restarting API service..."
	$(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.dev.override.yml --project-name $(DEV_PROJECT_NAME) down --remove-orphans
	$(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.dev.override.yml --project-name $(DEV_PROJECT_NAME) build --no-cache api
	$(DOCKER_CMD) compose -f docker-compose.yml -f docker-compose.dev.override.yml --project-name $(DEV_PROJECT_NAME) up -d

# ==============================================================================
# CODE QUALITY 
# ==============================================================================

.PHONY: format
format: ## Format code with black and ruff --fix
	@echo "Formatting code with black and ruff..."
	uv run black .
	uv run ruff check . --fix

.PHONY: lint
lint: ## Lint code with black check and ruff
	@echo "Linting code with black check and ruff..."
	uv run black --check .
	uv run ruff check .

# ==============================================================================
# TESTING
# ==============================================================================

.PHONY: test
test: local-test docker-test ## Run complete test suite (local SQLite then docker PostgreSQL)

# --- Local testing (lightweight, fast development) ---
.PHONY: local-test
local-test: unit-test sqlt-test ## Run lightweight local test suite (unit + SQLite DB tests)

.PHONY: unit-test
unit-test: ## Run unit tests locally
	@echo "🚀 Running unit tests (local)..."
	@uv run pytest tests/unit -v -s

.PHONY: sqlt-test
sqlt-test: ## Run database tests with SQLite (fast, lightweight, no docker)
	@echo "🚀 Running database tests with SQLite..."
	@USE_SQLITE=true uv run pytest tests/db -v -s

# --- Docker testing (production-like, comprehensive) ---
.PHONY: docker-test
docker-test: build-test pstg-test e2e-test ## Run all Docker-based tests

.PHONY: build-test
build-test: ## Build Docker image for testing without leaving artifacts
	@echo "Building Docker image for testing (clean build)..."
	@TEMP_IMAGE_TAG=$$(date +%s)-build-test; \
	$(DOCKER_CMD) build --target production --tag temp-build-test:$$TEMP_IMAGE_TAG . && \
	echo "Build successful. Cleaning up temporary image..." && \
	$(DOCKER_CMD) rmi temp-build-test:$$TEMP_IMAGE_TAG || true

.PHONY: pstg-test
pstg-test: ## Run database tests with PostgreSQL (robust, production-like)
	@echo "🚀 Starting TEST containers for PostgreSQL database test..."
	@USE_SQLITE=false $(TEST_COMPOSE) up -d --build
	@echo "Running database tests inside api container (against PostgreSQL)..."
	@USE_SQLITE=false $(TEST_COMPOSE) exec api pytest tests/db -v -s; \
	EXIT_CODE=$$?; \
	echo "🔴 Stopping TEST containers..."; \
	$(TEST_COMPOSE) down --remove-orphans; \
	exit $$EXIT_CODE

.PHONY: e2e-test
e2e-test: ## Run e2e tests against containerized application stack (runs from host)
	@echo "🚀 Running e2e tests (from host)..."
	@USE_SQLITE=false uv run pytest tests/e2e -v -s

# ==============================================================================
# CLEANUP
# ==============================================================================

.PHONY: clean
clean: ## Remove __pycache__ and .venv to make project lightweight
	@echo "🧹 Cleaning up project..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .venv
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@echo "✅ Cleanup completed"