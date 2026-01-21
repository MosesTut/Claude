# Timbuktoo MVP - Developer Guide

**Complete guide for developers working on the Timbuktoo Mobile MVP**

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Interactive Setup (Recommended)
```bash
./scripts/quick-start.sh
# Select "1) Full Setup (backend + mobile)"
```

### Option 2: Manual Setup
```bash
# Backend (Terminal 1)
cd backend
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
docker-compose up -d

# Mobile (Terminal 2)
cd mobile
npm install
npm start
# Press 'i' for iOS or 'a' for Android
```

### Option 3: Command Line
```bash
# Full setup in one command
./scripts/quick-start.sh --full

# Backend only
./scripts/quick-start.sh --backend

# Run tests
./scripts/quick-start.sh --test
```

---

## 📁 Project Structure

```
timbuktoo/
├── backend/                 # FastAPI + PostgreSQL backend
│   ├── app/
│   │   ├── api/            # REST API endpoints (8 routes)
│   │   ├── models/         # SQLAlchemy models (5 tables)
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── utils/          # Auth, AI client utilities
│   │   ├── main.py         # FastAPI application
│   │   ├── config.py       # Environment configuration
│   │   └── database.py     # Database connection
│   ├── alembic/            # Database migrations
│   ├── Dockerfile          # Backend Docker image
│   ├── docker-compose.yml  # PostgreSQL + FastAPI
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
│
├── mobile/                  # React Native + Expo mobile app
│   ├── src/
│   │   ├── screens/        # 10 mobile screens
│   │   ├── services/       # API client (Axios + JWT)
│   │   ├── config/         # API endpoints
│   │   ├── types/          # TypeScript interfaces
│   │   └── utils/          # Health check utilities
│   ├── App.tsx             # Root component + navigation
│   ├── app.json            # Expo configuration
│   ├── package.json        # npm dependencies
│   ├── tsconfig.json       # TypeScript config
│   └── .env.example        # Environment template
│
├── docs/                    # Complete documentation
│   ├── mobile/app-store/   # iOS + Android submission guides
│   ├── enterprise/         # Enterprise sales docs
│   ├── compliance/         # SOC 2, GDPR, CCPA
│   └── investor/           # Investor metrics dashboard
│
├── scripts/                 # Automation scripts
│   ├── quick-start.sh      # Interactive setup (recommended)
│   ├── test-backend.sh     # Backend API testing
│   └── deploy.sh           # Production deployment
│
├── .github/workflows/       # CI/CD pipeline
│   └── ci.yml              # GitHub Actions
│
├── TESTING.md              # Complete testing guide
├── LAUNCH_ROADMAP.md       # 6-8 week launch plan
├── CHANGELOG.md            # Version history
└── README.md               # Project overview
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15 (via Docker)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **AI**: Anthropic Claude 3.5 Sonnet
- **Auth**: JWT (HS256) with bcrypt
- **Deployment**: Docker + docker-compose

### Mobile
- **Framework**: React Native 0.72 + Expo 49
- **Language**: TypeScript 5.0
- **Navigation**: React Navigation 6
- **UI**: React Native Paper (Material Design)
- **HTTP**: Axios with interceptors
- **Storage**: Expo SecureStore (Keychain/Keystore)
- **Build**: EAS Build

### DevOps
- **CI/CD**: GitHub Actions
- **Containers**: Docker + docker-compose
- **Testing**: pytest (backend), Jest (mobile)
- **Linting**: flake8 (Python), ESLint (TypeScript)

---

## 📋 API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login with email/password
- `POST /auth/logout` - Logout (optional endpoint)

### Preferences
- `POST /preferences` - Save user travel preferences
- `GET /preferences` - Load saved preferences

### Cities (AI-Powered)
- `GET /cities/recommendations` - Get 3 AI-recommended cities (5-10s)

### Itineraries (AI-Powered)
- `POST /itinerary/generate` - Generate day-by-day itinerary (30-60s)
- `GET /itinerary/{id}` - Get specific itinerary
- `PATCH /itinerary/{id}/rating` - Rate itinerary (helpful/not helpful)

### Feedback
- `POST /feedback` - Submit feedback/report issue

### User Account
- `DELETE /user/account` - Delete account + all data (GDPR)

**API Documentation**: http://localhost:8000/docs (when running)

---

## 📱 Mobile Screens

### 1. SplashScreen
- Shows app logo + loading indicator
- Checks auth status on mount
- Auto-navigates to Onboarding (logged out) or Preferences (logged in)

### 2. OnboardingScreen
- Welcome screen with feature highlights
- Shows 3 benefits (AI-Powered, Discover Cities, Day-by-Day)
- Button → AI Disclosure screen

### 3. AIDisclosureScreen (CRITICAL)
- **Apple Guideline 5.1.1 Compliance**
- Mandatory consent checkbox: "I understand that itineraries are AI-generated"
- Blocks progress until checked
- Required for App Store approval

### 4. DataUseScreen
- Privacy and data use terms
- Checkbox: "I accept the terms"
- Button → Auth screen

### 5. AuthScreen
- Tabbed interface (Login / Sign Up)
- Email + password fields
- Validation (email format, password length ≥8)
- JWT token stored in SecureStore

### 6. PreferencesScreen
- Multi-select interests (Culture, Food, Nature, etc.)
- Multi-select food preferences (Vegetarian, Vegan, etc.)
- Budget level (Budget, Mid-Range, Luxury)
- Pace (Relaxed, Moderate, Packed)
- Trip length (1-30 days)
- Button → City Recommendations

### 7. CityRecommendationScreen
- Displays 3 AI-recommended cities
- Shows city name, country, reasoning, match score
- Selectable cards (border turns purple)
- Button → Generate Itinerary (30-60s)

### 8. ItineraryScreen (CRITICAL)
- **Apple Guideline 5.1.1 Compliance**
- **Yellow AI disclosure banner at top** (cannot dismiss)
- Day-by-day itinerary cards:
  - Morning activity (location, duration, tips)
  - Lunch recommendation (restaurant, cuisine, price, neighborhood)
  - Afternoon activity
  - Dinner recommendation
  - Evening activity (optional)
- General tips section
- Rating buttons (thumbs up/down)
- "Report an Issue" button → Feedback screen

### 9. FeedbackScreen (CRITICAL)
- **Apple Guideline 5.1.1 Compliance**
- 4 report types:
  - Inaccurate information
  - Inappropriate content
  - Missing information
  - Other
- Comments field (optional)
- Submit button
- Compliance team review (48-hour SLA)

### 10. SettingsScreen
- Account section (email display)
- Legal section (Privacy Policy, Terms of Service)
- Danger Zone → Delete My Data (GDPR compliant)
- Logout button

---

## 🧪 Testing

### Run All Tests
```bash
./scripts/quick-start.sh --test
```

### Backend Testing
```bash
# Python syntax check
cd backend
python3 -m py_compile app/**/*.py

# Manual API testing
./scripts/test-backend.sh

# Health check
curl http://localhost:8000/health
```

### Mobile Testing
```bash
# TypeScript check
cd mobile
npx tsc --noEmit

# Run on simulator
npm start
# Press 'i' for iOS or 'a' for Android
```

### End-to-End Testing
See `TESTING.md` for complete test cases (20+ scenarios)

---

## 🔑 Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://timbuktoo:password@localhost:5432/timbuktoo

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=30

# AI
ANTHROPIC_API_KEY=sk-ant-your-key-here  # REQUIRED

# CORS
CORS_ORIGINS=http://localhost:19000,http://localhost:19006,exp://localhost:19000

# Rate Limiting
FREE_TIER_ITINERARY_LIMIT=3
```

### Mobile (.env)
```bash
# API
API_BASE_URL=http://localhost:8000

# For physical device (replace with your computer's IP)
# API_BASE_URL=http://192.168.1.100:8000
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Problem**: Port 8000 already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Problem**: PostgreSQL won't start
```bash
# Remove volumes and restart
cd backend
docker-compose down -v
docker-compose up -d
```

**Problem**: Missing ANTHROPIC_API_KEY
```bash
# Add to backend/.env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> backend/.env
```

### Mobile Won't Connect to Backend

**Problem**: Network error when calling API
```bash
# Check backend is running
curl http://localhost:8000/health

# For physical device, use computer's IP in mobile/.env
# Find your IP: ifconfig (macOS/Linux) or ipconfig (Windows)
```

**Problem**: Module not found errors
```bash
cd mobile
rm -rf node_modules
npm install
```

### Database Issues

**Problem**: Migration failed
```bash
cd backend
docker-compose down -v  # CAUTION: Deletes all data
docker-compose up -d
alembic upgrade head
```

**Problem**: Connection refused
```bash
# Check PostgreSQL is running
docker-compose ps postgres
```

---

## 🚢 Deployment

### Backend Deployment (Heroku)

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS

# Login
heroku login

# Create app
heroku create timbuktoo-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=sk-ant-your-key-here
heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32)

# Deploy
git push heroku claude/build-timbuktoo-mvp-TKxPc:main

# Run migrations
heroku run alembic upgrade head
```

### Mobile Deployment (EAS Build)

```bash
cd mobile

# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Configure
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to App Store
eas submit --platform ios

# Submit to Google Play
eas submit --platform android
```

---

## 📊 Monitoring

### Backend Health Check
```bash
# Health endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy","database":"connected"}

# API metrics
curl http://localhost:8000/metrics  # Prometheus metrics (if enabled)
```

### Database Status
```bash
cd backend
docker-compose ps postgres
docker-compose logs -f postgres
```

### Mobile Debugging
```bash
# Expo DevTools
npm start
# Press 'd' to open DevTools
# Press 'm' to toggle menu in simulator
# Shake device to open menu on physical device
```

---

## 🔒 Security & Compliance

### Apple App Store Compliance
✅ **Guideline 5.1.1 (AI Disclosure)**
- Mandatory consent checkbox (AIDisclosureScreen)
- AI banner on every itinerary
- Feedback mechanism (FeedbackScreen with 4 report types)

### GDPR Compliance
✅ **Article 17 (Right to Erasure)**
- Delete My Data button (SettingsScreen)
- Complete account deletion (30-day SLA)
- All user data removed from database

### CCPA Compliance
✅ **California Consumer Privacy Act**
- Privacy Policy accessible (SettingsScreen)
- Data deletion available
- No data selling

### Data Security
✅ **Encryption**
- JWT tokens with HS256
- Passwords hashed with bcrypt (12 rounds)
- Tokens stored in SecureStore (Keychain/Keystore)

---

## 📈 Performance Targets

### Backend
- Login/Signup: <500ms
- Preferences save: <300ms
- City recommendations: 5-10 seconds (AI)
- Itinerary generation: 30-60 seconds (AI)
- Uptime: 99.9%

### Mobile
- App launch: <2 seconds
- Screen navigation: <300ms
- Crash-free rate: >99.5%

### Database
- Query response: <100ms
- Connection pool: 5-20 connections
- Backup frequency: Daily

---

## 🎯 Next Steps

### For Development
1. ✅ Run `./scripts/quick-start.sh` to set up environment
2. ✅ Test signup → preferences → cities → itinerary flow
3. ✅ Read `TESTING.md` for complete test cases
4. ✅ Fix any bugs found
5. ✅ Add automated tests (pytest, Jest)

### For App Store Submission
1. ✅ Create 5 screenshots (see `docs/mobile/app-store/Screenshot_Requirements.md`)
2. ✅ Build production apps (EAS Build)
3. ✅ Test with reviewer account (reviewer@timbuktoo.ai / ReviewTest2024!)
4. ✅ Submit to App Store + Google Play
5. ✅ Monitor reviews and respond within 48 hours

### For Production Launch
1. ✅ Deploy backend to Heroku/AWS
2. ✅ Set up Firebase Crashlytics
3. ✅ Configure Datadog monitoring
4. ✅ Set up PagerDuty alerts
5. ✅ Launch marketing website (timbuktoo.app)

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Testing Guide**: `TESTING.md`
- **Launch Roadmap**: `LAUNCH_ROADMAP.md`
- **App Store Guides**: `docs/mobile/app-store/`
- **Enterprise Docs**: `docs/enterprise/`
- **CI/CD Pipeline**: `.github/workflows/ci.yml`

---

## 🆘 Getting Help

### Issues
Report bugs at: https://github.com/MosesTut/Claude/issues

### Questions
- Read this guide + `TESTING.md` first
- Check `LAUNCH_ROADMAP.md` for timeline questions
- Review API docs at http://localhost:8000/docs

---

**Last Updated**: 2025-01-21
**Status**: Ready for Development ✅
**Version**: 1.0.0 (MVP)
