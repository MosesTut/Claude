#!/bin/bash
# Deploy Timbuktoo MVP

set -e

echo "Deploying Timbuktoo Travel Concierge MVP..."

# Check environment
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example and configure."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
bash scripts/init_database.sh

# Load pilot data
echo "Loading pilot city data..."
python scripts/load_pilot_data.py

# Start monitoring
echo "Starting Prometheus metrics server..."
# This would typically be in a separate process/container

echo "Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Review configuration in config/timbuktoo.yaml"
echo "2. Set up API keys in .env file"
echo "3. Test the system with scripts/test_workflow.py"
echo "4. Start the API server (if applicable)"
