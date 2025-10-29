#!/bin/bash
set -e

# Ejecutar migraciones
echo "Running Alembic migrations..."
alembic upgrade head

# Iniciar FastAPI
echo "Starting FastAPI..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --proxy-headers