#!/bin/sh

# Exit immediately if a command exits with a non-zero status ('e')
# or if an unset variable is used ('u').
set -eu

# Activate the virtual environment.
. /app/.venv/bin/activate

# --- Run database migrations if starting server ---
if [ "$#" -eq 0 ] || [ "$1" = "uvicorn" ]; then
    echo "Running database migrations..."
    alembic upgrade head || echo "No migrations to run or database not configured"
fi

# --- Start Uvicorn server (or run another command) ---
# If arguments are passed to the script, execute them instead of the default server.
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    echo "Starting server on 0.0.0.0:8000 with 1 worker(s)..."
    exec uvicorn src.main:app \
        --host "0.0.0.0" \
        --port "8000" \
        --workers "1"
fi
