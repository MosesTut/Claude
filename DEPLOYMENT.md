# Timbuktoo Backend Deployment Guide

This guide covers deploying the Timbuktoo backend API to production using Heroku or Railway.

## Prerequisites

- Git repository with all code committed
- Anthropic API key (get from https://console.anthropic.com)
- Heroku or Railway account

## Option 1: Deploy to Heroku (Recommended for beginners)

### Cost: ~$25-50/month
- **Eco Dynos**: $5/month (or $7 with database)
- **Mini PostgreSQL**: $5/month
- **Total**: ~$12/month minimum

### Step 1: Install Heroku CLI

```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login to Heroku

```bash
heroku login
```

### Step 3: Run Deployment Script

```bash
./scripts/deploy-heroku.sh
```

The script will:
1. Create Heroku app
2. Add PostgreSQL database
3. Set environment variables
4. Deploy code
5. Run database migrations
6. Provide your API URL

### Step 4: Update Mobile App

Update `mobile/.env`:
```bash
API_BASE_URL=https://your-app-name.herokuapp.com
```

### Step 5: Verify Deployment

```bash
# Check health endpoint
curl https://your-app-name.herokuapp.com/health

# View logs
heroku logs --tail --app your-app-name

# Open dashboard
heroku open --app your-app-name
```

---

## Option 2: Deploy to Railway (Modern alternative)

### Cost: Pay-as-you-go, ~$5-20/month
- **Free $5 credit/month**
- **$0.000463/GB-hour** for compute
- **$0.25/GB** for PostgreSQL storage

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Run Deployment Script

```bash
./scripts/deploy-railway.sh
```

The script will:
1. Create Railway project
2. Add PostgreSQL database
3. Set environment variables
4. Deploy code
5. Generate public URL

### Step 4: Run Database Migrations

```bash
railway run alembic upgrade head
```

### Step 5: Update Mobile App

Update `mobile/.env`:
```bash
API_BASE_URL=https://your-project.railway.app
```

### Step 6: Verify Deployment

```bash
# Check health endpoint
curl https://your-project.railway.app/health

# View logs
railway logs

# Open dashboard
railway open
```

---

## Manual Deployment (For advanced users)

If you prefer manual setup or want to use a different provider:

### 1. Environment Variables

Set these in your hosting platform:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...
JWT_SECRET=<random-64-char-hex-string>
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Optional (with defaults)
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720
ENVIRONMENT=production
```

### 2. Database Setup

```bash
# Run migrations
alembic upgrade head
```

### 3. Start Server

```bash
# Production server
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key | `sk-ant-api03-...` |
| `JWT_SECRET` | Yes | Secret for signing JWT tokens | `<64-char-hex>` |
| `DATABASE_URL` | Auto* | PostgreSQL connection URL | `postgresql://...` |
| `JWT_ALGORITHM` | No | JWT signing algorithm | `HS256` |
| `JWT_EXPIRATION_HOURS` | No | Token expiration time | `720` (30 days) |
| `ENVIRONMENT` | No | Environment name | `production` |
| `PORT` | Auto* | Server port | `8000` |

*Auto-set by Heroku/Railway

---

## Post-Deployment Checklist

- [ ] ✅ Health endpoint returns `{"status":"healthy"}`
- [ ] ✅ Database connection successful
- [ ] ✅ `/docs` (Swagger UI) is accessible
- [ ] ✅ Test signup endpoint: `POST /auth/signup`
- [ ] ✅ Test login endpoint: `POST /auth/login`
- [ ] ✅ Mobile app can connect to API
- [ ] ✅ Logs show no errors
- [ ] ✅ Environment variables set correctly

---

## Testing Your Deployment

### 1. Test Health Endpoint

```bash
curl https://your-api-url/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Test Signup

```bash
curl -X POST https://your-api-url/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "ai_disclosure_accepted": true,
    "data_use_accepted": true
  }'
```

Expected response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "test@example.com"
  }
}
```

### 3. View API Documentation

Visit: `https://your-api-url/docs`

---

## Troubleshooting

### Database Connection Errors

```bash
# Heroku: Check database URL
heroku config:get DATABASE_URL --app your-app

# Railway: Check logs
railway logs
```

### Migration Failures

```bash
# Heroku: Run migrations manually
heroku run alembic upgrade head --app your-app

# Railway: Run migrations
railway run alembic upgrade head
```

### Application Crashes

```bash
# View logs
heroku logs --tail --app your-app  # Heroku
railway logs                        # Railway

# Common issues:
# 1. Missing ANTHROPIC_API_KEY
# 2. Invalid DATABASE_URL
# 3. Port binding issues (ensure $PORT is used)
```

### API Not Responding

1. Check if dyno/service is running
2. Verify domain/URL is correct
3. Check logs for startup errors
4. Ensure database migrations ran successfully

---

## Monitoring & Maintenance

### View Application Logs

```bash
# Heroku
heroku logs --tail --app your-app

# Railway
railway logs --follow
```

### Database Backups

```bash
# Heroku (automatic daily backups on paid plans)
heroku pg:backups:capture --app your-app
heroku pg:backups:download --app your-app

# Railway (configure in dashboard)
```

### Scale Application

```bash
# Heroku: Upgrade dyno tier
heroku ps:scale web=1:standard-1x --app your-app

# Railway: Adjust in dashboard
railway settings
```

---

## Updating Your Deployment

### Deploy New Code

```bash
# Commit changes
git add .
git commit -m "Update: description"

# Push to Heroku
git push heroku claude/build-timbuktoo-mvp-TKxPc:main

# Push to Railway
railway up
```

### Run New Migrations

```bash
# Heroku
heroku run alembic upgrade head --app your-app

# Railway
railway run alembic upgrade head
```

---

## Cost Optimization

### Heroku
- **Eco dynos**: $5/month (sleeps after 30min inactivity)
- **Basic dynos**: $7/month (never sleeps)
- **Mini PostgreSQL**: $5/month
- **Tip**: Start with Eco, upgrade if needed

### Railway
- **Free tier**: $5 credit/month (enough for testing)
- **Usage-based**: Only pay for what you use
- **Tip**: Monitor usage in dashboard

---

## Security Best Practices

1. **Use strong JWT secrets**: Generate with `openssl rand -hex 32`
2. **Enable HTTPS**: Automatic on Heroku/Railway
3. **Rotate API keys**: If compromised, rotate immediately
4. **Monitor logs**: Check for suspicious activity
5. **Keep dependencies updated**: Run `pip install -U` regularly

---

## Support

**Heroku Issues**: https://help.heroku.com
**Railway Issues**: https://railway.app/help
**Timbuktoo Issues**: GitHub Issues

---

## Next Steps After Deployment

1. ✅ Update mobile app with production API URL
2. ✅ Test all user flows end-to-end
3. ✅ Set up error monitoring (Sentry, Bugsnag)
4. ✅ Configure custom domain (optional)
5. ✅ Set up CI/CD for automated deployments
6. ✅ Create staging environment for testing
