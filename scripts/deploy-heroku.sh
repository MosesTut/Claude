#!/bin/bash

# Timbuktoo Heroku Deployment Script
# This script automates the deployment of the Timbuktoo backend to Heroku

set -e  # Exit on any error

echo "🚀 Timbuktoo Heroku Deployment"
echo "================================"
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Error: Heroku CLI is not installed"
    echo "📥 Install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "❌ Error: Not logged in to Heroku"
    echo "🔐 Please run: heroku login"
    exit 1
fi

# Get app name from user
read -p "Enter Heroku app name (e.g., timbuktoo-backend): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ Error: App name cannot be empty"
    exit 1
fi

# Check if app already exists
if heroku apps:info --app "$APP_NAME" &> /dev/null; then
    echo "ℹ️  App '$APP_NAME' already exists"
    read -p "Deploy to existing app? (y/n): " DEPLOY_EXISTING
    if [ "$DEPLOY_EXISTING" != "y" ]; then
        echo "Aborted"
        exit 0
    fi
else
    echo "📦 Creating Heroku app: $APP_NAME"
    heroku create "$APP_NAME"
fi

# Add PostgreSQL addon
echo "🗄️  Adding PostgreSQL database..."
if ! heroku addons:info heroku-postgresql --app "$APP_NAME" &> /dev/null; then
    heroku addons:create heroku-postgresql:mini --app "$APP_NAME"
    echo "✅ PostgreSQL database added"
else
    echo "ℹ️  PostgreSQL database already exists"
fi

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
heroku config:set \
    ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    JWT_SECRET="$JWT_SECRET" \
    JWT_ALGORITHM="HS256" \
    JWT_EXPIRATION_HOURS="720" \
    ENVIRONMENT="production" \
    --app "$APP_NAME"

echo "✅ Environment variables configured"

# Deploy code
echo ""
echo "🚢 Deploying code to Heroku..."
git push heroku claude/build-timbuktoo-mvp-TKxPc:main

# Run database migrations
echo ""
echo "🔄 Running database migrations..."
heroku run alembic upgrade head --app "$APP_NAME"

# Check if deployment was successful
echo ""
echo "🔍 Checking deployment status..."
if heroku ps --app "$APP_NAME" | grep -q "web.*up"; then
    echo "✅ Deployment successful!"

    # Get app URL
    APP_URL=$(heroku apps:info --app "$APP_NAME" | grep "Web URL" | awk '{print $3}')

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🎉 Deployment Complete!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📱 Your API is now live at:"
    echo "   $APP_URL"
    echo ""
    echo "🔗 Test your API:"
    echo "   curl ${APP_URL}health"
    echo ""
    echo "📊 View logs:"
    echo "   heroku logs --tail --app $APP_NAME"
    echo ""
    echo "⚙️  Open dashboard:"
    echo "   heroku open --app $APP_NAME"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Update mobile/.env with: API_BASE_URL=$APP_URL"
    echo "   2. Test API endpoints"
    echo "   3. Monitor logs for any issues"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ Deployment may have failed. Check logs:"
    echo "   heroku logs --tail --app $APP_NAME"
    exit 1
fi
