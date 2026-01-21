#!/bin/bash

# Timbuktoo Railway Deployment Script
# This script automates the deployment of the Timbuktoo backend to Railway

set -e  # Exit on any error

echo "🚀 Timbuktoo Railway Deployment"
echo "================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Error: Railway CLI is not installed"
    echo "📥 Install from: https://docs.railway.app/develop/cli"
    echo "   npm install -g @railway/cli"
    exit 1
fi

# Check if logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "❌ Error: Not logged in to Railway"
    echo "🔐 Please run: railway login"
    exit 1
fi

# Initialize Railway project
echo "📦 Initializing Railway project..."
read -p "Create new Railway project? (y/n): " CREATE_NEW

if [ "$CREATE_NEW" = "y" ]; then
    read -p "Enter project name (e.g., timbuktoo-backend): " PROJECT_NAME
    railway init --name "$PROJECT_NAME"
    echo "✅ Project created"
else
    railway link
fi

# Add PostgreSQL database
echo ""
echo "🗄️  Adding PostgreSQL database..."
railway add --database postgres
echo "✅ PostgreSQL database added"

# Get Anthropic API key
echo ""
echo "🔑 Setting up environment variables..."
read -p "Enter your Anthropic API key (sk-ant-...): " ANTHROPIC_API_KEY

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: Anthropic API key is required"
    exit 1
fi

# Generate secure JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Set environment variables
echo "📝 Configuring environment variables..."
railway variables set ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
railway variables set JWT_SECRET="$JWT_SECRET"
railway variables set JWT_ALGORITHM="HS256"
railway variables set JWT_EXPIRATION_HOURS="720"
railway variables set ENVIRONMENT="production"

echo "✅ Environment variables configured"

# Deploy code
echo ""
echo "🚢 Deploying to Railway..."
railway up

# Get deployment URL
echo ""
echo "🔍 Getting deployment URL..."
DEPLOYMENT_URL=$(railway domain)

if [ -z "$DEPLOYMENT_URL" ]; then
    echo "⚠️  No domain assigned yet. Generating domain..."
    railway domain
    DEPLOYMENT_URL=$(railway domain)
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Your API is now live at:"
echo "   https://$DEPLOYMENT_URL"
echo ""
echo "🔗 Test your API:"
echo "   curl https://${DEPLOYMENT_URL}/health"
echo ""
echo "📊 View logs:"
echo "   railway logs"
echo ""
echo "⚙️  Open dashboard:"
echo "   railway open"
echo ""
echo "📝 Next steps:"
echo "   1. Update mobile/.env with: API_BASE_URL=https://$DEPLOYMENT_URL"
echo "   2. Test API endpoints"
echo "   3. Run database migrations:"
echo "      railway run alembic upgrade head"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
