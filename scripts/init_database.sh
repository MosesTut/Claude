#!/bin/bash
# Initialize Timbuktoo database

set -e

echo "Initializing Timbuktoo database..."

# Check if PostgreSQL is available
if ! command -v psql &> /dev/null; then
    echo "Error: PostgreSQL client not found. Please install PostgreSQL."
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Create database if it doesn't exist
echo "Creating database..."
createdb timbuktoo || echo "Database may already exist"

# Run migrations
echo "Running migrations..."
psql $DATABASE_URL -f timbuktoo/database/migrations/001_initial_schema.sql

echo "Database initialized successfully!"
