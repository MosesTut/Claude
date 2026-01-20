# Timbuktoo Mobile MVP - Launch Roadmap (Documentation → Live Platform)

**Last Updated**: 2024-07-16
**Purpose**: Critical path from specs to production launch with paying customers
**Timeline**: 6-8 weeks (assuming 2-3 full-time engineers)

---

## Current Status: Documentation Complete ✅

**What We Have**:
- ✅ Complete mobile app specifications (10 screens, 47 files documented)
- ✅ Backend API specifications (8 endpoints, FastAPI)
- ✅ App Store submission package (listing copy, screenshots, legal docs)
- ✅ Enterprise sales package (Trust Portal, pricing, security)
- ✅ Growth experiments plan (5 tests)
- ✅ Revenue forecasting model

**What We DON'T Have Yet**:
- ❌ Actual working code (mobile app, backend API)
- ❌ Deployed infrastructure (database, servers, AI integration)
- ❌ App Store approval (apps not submitted yet)
- ❌ Payment processing setup (Stripe, RevenueCat)
- ❌ Monitoring and operations (crash reporting, alerting)
- ❌ Marketing website (landing page, conversion funnel)

---

## Launch Roadmap (6-8 Weeks)

### Phase 1: Infrastructure & Backend (Week 1-2)

**Priority: P0 (Must Have)**

#### 1.1 Database Setup
**Status**: ❌ Not Started
**Owner**: Backend Engineer
**Timeline**: 2 days

**Tasks**:
- [ ] Provision PostgreSQL database (AWS RDS or Supabase)
  - Instance size: db.t3.small (start small, scale up)
  - Storage: 20 GB (General Purpose SSD)
  - Multi-AZ: No (for MVP, enable later)
  - Backup: Daily automated snapshots (30-day retention)
- [ ] Create database schemas (run SQL migrations):
  ```sql
  CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    platform VARCHAR(10) -- 'mobile', 'web'
  );

  CREATE TABLE preferences (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    interests TEXT[], -- ['culture', 'food', 'nature']
    food_preference VARCHAR(50), -- 'adventurous', 'vegetarian', 'vegan'
    budget VARCHAR(20), -- 'low', 'medium', 'high', 'luxury'
    dates JSONB -- { start: '2024-08-01', end: '2024-08-10' }
  );

  CREATE TABLE itineraries (
    itinerary_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    city_id VARCHAR(100),
    city_name VARCHAR(255),
    itinerary JSONB, -- Full itinerary JSON
    created_at TIMESTAMP DEFAULT NOW()
  );

  CREATE TABLE feedback (
    feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    itinerary_id UUID REFERENCES itineraries(itinerary_id),
    rating VARCHAR(20), -- 'helpful', 'not-helpful'
    report_type VARCHAR(50), -- 'inaccurate', 'inappropriate', 'missing', 'other'
    comments TEXT,
    created_at TIMESTAMP DEFAULT NOW()
  );

  CREATE TABLE subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    platform VARCHAR(10), -- 'ios', 'android'
    product_id VARCHAR(100), -- 'pro_monthly', 'pro_annual'
    status VARCHAR(20), -- 'active', 'expired', 'cancelled'
    starts_at TIMESTAMP,
    expires_at TIMESTAMP,
    auto_renew BOOLEAN DEFAULT TRUE
  );
  ```
- [ ] Set up database connection pooling (PgBouncer or SQLAlchemy pool)
- [ ] Create read-only replica (optional for MVP, add later)

**Validation**:
```bash
# Test database connection
psql -h <RDS_ENDPOINT> -U postgres -d timbuktoo
# Run migrations
alembic upgrade head
# Verify tables created
\dt
```

---

#### 1.2 Backend API Implementation
**Status**: ❌ Not Started
**Owner**: Backend Engineer
**Timeline**: 5 days

**Tasks**:
- [ ] Set up FastAPI project structure:
  ```
  timbuktoo-backend/
  ├── app/
  │   ├── main.py (FastAPI app)
  │   ├── api/
  │   │   ├── auth.py (signup, login)
  │   │   ├── preferences.py (save/load preferences)
  │   │   ├── cities.py (city recommendations)
  │   │   ├── itineraries.py (generate itinerary)
  │   │   └── feedback.py (submit feedback)
  │   ├── models/ (SQLAlchemy models)
  │   ├── schemas/ (Pydantic schemas)
  │   └── utils/ (JWT, bcrypt, helpers)
  ├── requirements.txt
  └── Dockerfile
  ```

- [ ] Implement authentication endpoints (see `mobile/IMPLEMENTATION_GUIDE.md`):
  - POST /api/v1/auth/signup (email + password, JWT generation)
  - POST /api/v1/auth/login (authentication)
  - POST /api/v1/auth/logout (optional token blacklist)

- [ ] Implement preferences endpoints:
  - GET /api/v1/preferences (load user preferences)
  - POST /api/v1/preferences (save preferences)

- [ ] Implement city recommendation endpoint (STUB for now):
  - GET /api/v1/cities/recommendations
  - **MVP**: Return hardcoded 3 cities (Barcelona, Tokyo, Lisbon)
  - **Later**: Integrate with City Selection Agent

- [ ] Implement itinerary generation endpoint (STUB for now):
  - POST /api/v1/itinerary/generate
  - **MVP**: Return mock itinerary JSON
  - **Later**: Integrate with multi-agent workflow

- [ ] Implement feedback endpoint:
  - POST /api/v1/feedback (save feedback to database)

**Validation**:
```bash
# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test endpoints
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Should return JWT token
```

**Deployment** (Week 2):
- [ ] Deploy to AWS EC2 or Heroku (for MVP)
- [ ] Set up HTTPS with Let's Encrypt
- [ ] Configure environment variables (DATABASE_URL, JWT_SECRET, ANTHROPIC_API_KEY)
- [ ] Set up health check endpoint (GET /health)

---

#### 1.3 AI Integration (Anthropic Claude API)
**Status**: ❌ Not Started
**Owner**: Backend Engineer
**Timeline**: 3 days

**Tasks**:
- [ ] Sign up for Anthropic API access (https://console.anthropic.com)
- [ ] Get API key (store in environment variables)
- [ ] Install Anthropic SDK:
  ```bash
  pip install anthropic
  ```
- [ ] Implement City Selection Agent:
  ```python
  import anthropic

  def get_city_recommendations(user_preferences):
      client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

      prompt = f"""
      User preferences:
      - Interests: {user_preferences['interests']}
      - Food: {user_preferences['food']}
      - Budget: {user_preferences['budget']}

      Recommend 3 cities that match these preferences. For each city, provide:
      - City name
      - Country
      - Reasoning (2-3 sentences explaining why this city matches)

      Return JSON format:
      {{
        "cities": [
          {{"city": "Barcelona", "country": "Spain", "reasoning": "..."}},
          ...
        ]
      }}
      """

      response = client.messages.create(
          model="claude-3-5-sonnet-20241022",
          max_tokens=1024,
          messages=[{"role": "user", "content": prompt}]
      )

      return response.content[0].text
  ```

- [ ] Implement Itinerary Generation Agent (Local Expert + Concierge):
  ```python
  def generate_itinerary(city_id, user_preferences):
      # Agent 1: Local Expert (research city)
      local_expert_prompt = f"Research {city_id} for a {user_preferences['budget']} budget traveler..."

      # Agent 2: Concierge (generate day-by-day plan)
      concierge_prompt = f"Create a 5-day itinerary for {city_id}..."

      # Return structured JSON
      return {
          "city": city_id,
          "days": [
              {
                  "day": 1,
                  "breakfast": {"name": "La Boqueria Market", "price": "$$"},
                  "activities": ["Sagrada Familia", "Park Güell"],
                  "lunch": {"name": "Cervecería Catalana", "price": "$$"},
                  "dinner": {"name": "Tickets Bar", "price": "$$$"}
              },
              # ... more days
          ]
      }
  ```

- [ ] Add rate limiting (3 itineraries per user per month for free tier)
- [ ] Add timeout handling (30-60 seconds for AI generation)
- [ ] Add error handling (retry with exponential backoff)

**Validation**:
```bash
# Test city recommendations
curl -X GET http://localhost:8000/api/v1/cities/recommendations \
  -H "Authorization: Bearer <JWT_TOKEN>"

# Test itinerary generation
curl -X POST http://localhost:8000/api/v1/itinerary/generate \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"cityId":"barcelona"}'
```

---

### Phase 2: Mobile App Development (Week 2-4)

**Priority: P0 (Must Have)**

#### 2.1 React Native App Setup
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 1 day

**Tasks**:
- [ ] Initialize React Native + Expo project:
  ```bash
  npx create-expo-app timbuktoo-mobile --template blank-typescript
  cd timbuktoo-mobile
  npm install @react-navigation/native @react-navigation/native-stack
  npm install expo-secure-store axios react-native-paper
  ```

- [ ] Set up project structure (see `mobile/IMPLEMENTATION_GUIDE.md`):
  ```
  mobile/
  ├── App.tsx
  ├── app.json
  ├── package.json
  ├── src/
  │   ├── screens/ (10 screens)
  │   ├── navigation/
  │   ├── api/ (API client)
  │   ├── utils/ (helpers)
  │   └── types/ (TypeScript types)
  ```

- [ ] Configure environment variables:
  ```typescript
  // .env
  API_BASE_URL=https://api.timbuktoo.app
  ```

---

#### 2.2 Implement Core Screens
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 8 days

**Tasks**:
- [ ] **Day 1**: Splash Screen + Welcome Screen
- [ ] **Day 2**: AI Disclosure Screen (CRITICAL - mandatory checkbox)
- [ ] **Day 3**: Data Use Screen + Auth Screen (login/signup)
- [ ] **Day 4**: Preferences Screen (interests, food, budget, dates)
- [ ] **Day 5**: City Recommendation Screen (3 cities)
- [ ] **Day 6**: Itinerary Screen (day-by-day with AI banner)
- [ ] **Day 7**: Feedback Screen (rating + report mechanism)
- [ ] **Day 8**: Settings Screen (Privacy Policy, Terms, Delete My Data)

**Reference**: Use `mobile/IMPLEMENTATION_GUIDE.md` for complete code examples for each screen.

**Validation**:
```bash
# Run on iOS simulator
npx expo start --ios

# Run on Android emulator
npx expo start --android

# Test each screen manually
```

---

#### 2.3 Integrate with Backend API
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 2 days

**Tasks**:
- [ ] Create API client with JWT interceptor:
  ```typescript
  import axios from 'axios';
  import * as SecureStore from 'expo-secure-store';

  const apiClient = axios.create({
    baseURL: process.env.API_BASE_URL,
    timeout: 30000,
  });

  // Add JWT token to all requests
  apiClient.interceptors.request.use(async (config) => {
    const token = await SecureStore.getItemAsync('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  export default apiClient;
  ```

- [ ] Implement API functions (see `mobile/src/api/`):
  - authAPI.signup(email, password)
  - authAPI.login(email, password)
  - preferencesAPI.savePreferences(token, preferences)
  - citiesAPI.getRecommendations(token)
  - itineraryAPI.generateItinerary(token, cityId)
  - feedbackAPI.submitFeedback(token, feedback)

- [ ] Test end-to-end flow:
  1. Signup → JWT token stored in SecureStore
  2. Login → JWT token retrieved
  3. Save preferences → API call succeeds
  4. Get city recommendations → 3 cities returned
  5. Generate itinerary → Full itinerary returned (30-60 seconds)
  6. Submit feedback → Success message

---

### Phase 3: App Store Submission (Week 4-5)

**Priority: P0 (Must Have)**

#### 3.1 Create Screenshots
**Status**: ❌ Not Started
**Owner**: Designer + Mobile Engineer
**Timeline**: 2 days

**Tasks**:
- [ ] Use `mobile/app-store/Screenshot_Requirements.md` as guide
- [ ] Create 5 iOS screenshots (1290×2796 pixels):
  1. AI Disclosure (MUST show checkbox unchecked)
  2. Preferences
  3. City Recommendations
  4. Itinerary (MUST show AI banner)
  5. Feedback

- [ ] Create 4-6 Android screenshots (1080×1920 pixels)
- [ ] Add overlays and captions (use `Screenshot_Captions.md`)
- [ ] Validate on real devices (no truncation, readable text)

**Tools**:
- Real device screenshots (iPhone 15 Pro Max, Pixel 5)
- OR use Figma with device frames
- OR use Screenshot Studio app

---

#### 3.2 Build Production Apps
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 2 days

**iOS Build**:
```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS Build
eas build:configure

# Build for iOS
eas build --platform ios --profile production

# Download IPA
eas build:download --platform ios

# Upload to App Store Connect via Transporter or Xcode
```

**Android Build**:
```bash
# Build AAB
eas build --platform android --profile production

# Download AAB
eas build:download --platform android

# Upload to Google Play Console
```

**Alternative** (Manual builds):
- iOS: Xcode → Product → Archive → Upload to App Store Connect
- Android: Android Studio → Build → Generate Signed Bundle

---

#### 3.3 Submit to App Stores
**Status**: ❌ Not Started
**Owner**: Product Manager
**Timeline**: 2 days (preparation) + 24-72 hours (review)

**iOS Submission**:
- [ ] Copy listing copy from `iOS_App_Store_Listing.md`
- [ ] Upload 5 screenshots
- [ ] Upload Privacy Nutrition Label (use `iOS_Privacy_Nutrition_Label.json`)
- [ ] Add demo account (reviewer@timbuktoo.ai / ReviewTest2024!)
- [ ] Add App Review Notes (use `App_Review_Notes.txt`)
- [ ] Submit for review

**Android Submission**:
- [ ] Copy listing copy from `Google_Play_Store_Listing.md`
- [ ] Upload 4-6 screenshots
- [ ] Complete Data Safety form (use `Google_Play_Console_Policy_Answers.md`)
- [ ] Add demo account
- [ ] Upload to Internal Testing Track (14-day minimum testing period)
- [ ] After 14 days, promote to Production

**Expected Timeline**:
- iOS: 24-72 hours for review (90% approved on first submission if following guide)
- Android: 24-48 hours for review

---

### Phase 4: Payment Processing (Week 5)

**Priority: P1 (Nice to Have for MVP, can launch without)**

#### 4.1 Set Up RevenueCat
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 2 days

**Tasks**:
- [ ] Sign up for RevenueCat (https://www.revenuecat.com)
- [ ] Create project "Timbuktoo Mobile"
- [ ] Add iOS app (Bundle ID: ai.timbuktoo.mobile)
- [ ] Add Android app (Package: ai.timbuktoo.mobile)
- [ ] Configure products in App Store Connect:
  - Product ID: ai.timbuktoo.mobile.pro.monthly ($9.99/month)
  - Product ID: ai.timbuktoo.mobile.pro.annual ($79.99/year)
- [ ] Configure products in Google Play Console:
  - Product ID: pro_monthly ($9.99/month)
  - Product ID: pro_annual ($79.99/year)
- [ ] Install RevenueCat SDK:
  ```bash
  npm install react-native-purchases
  cd ios && pod install && cd ..
  ```
- [ ] Implement paywall (use `IAP_Implementation_Guide.md`)

**MVP Decision**: Can launch without IAP and add later. Free tier allows 3 itineraries/month.

---

### Phase 5: Monitoring & Operations (Week 5-6)

**Priority: P0 (Must Have Before Launch)**

#### 5.1 Crash Reporting
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 1 day

**Tasks**:
- [ ] Set up Firebase Crashlytics (use `Crash_Reporting_Setup.md`)
- [ ] Add to iOS: Update Podfile, add GoogleService-Info.plist
- [ ] Add to Android: Update build.gradle, add google-services.json
- [ ] Initialize in App.tsx:
  ```typescript
  import crashlytics from '@react-native-firebase/crashlytics';

  useEffect(() => {
    crashlytics().setCrashlyticsCollectionEnabled(true);
  }, []);
  ```
- [ ] Test crash reporting (force crash, verify in Firebase Console)
- [ ] Remove test crash code before production

---

#### 5.2 Analytics
**Status**: ❌ Not Started
**Owner**: Mobile Engineer
**Timeline**: 1 day

**Tasks**:
- [ ] Set up Firebase Analytics (included with Crashlytics)
- [ ] Track key events:
  - user_signup
  - first_itinerary_generated
  - paywall_viewed
  - trial_started
  - feedback_submitted
- [ ] Test events in Firebase Console → DebugView

---

#### 5.3 Backend Monitoring
**Status**: ❌ Not Started
**Owner**: Backend Engineer
**Timeline**: 1 day

**Tasks**:
- [ ] Set up Datadog or CloudWatch for API monitoring
- [ ] Add health check endpoint (GET /health)
- [ ] Set up uptime monitoring (Pingdom or UptimeRobot)
- [ ] Configure PagerDuty for on-call alerts
- [ ] Set up Slack alerts for P0/P1 incidents

---

### Phase 6: Marketing & Growth (Week 6-8)

**Priority: P1 (Nice to Have, but critical for customer acquisition)**

#### 6.1 Landing Page
**Status**: ❌ Not Started
**Owner**: Designer + Frontend Engineer
**Timeline**: 3 days

**Tasks**:
- [ ] Create landing page (https://timbuktoo.app):
  - Hero: "Your AI Travel Concierge" + Download buttons
  - Features: AI-powered, personalized, easy to use
  - Screenshots: Show app in action
  - Social proof: "Join 10,000+ travelers" (once you have users)
  - Footer: Privacy Policy, Terms of Service, Trust Center

- [ ] Set up analytics (Google Analytics or Plausible)
- [ ] Add email capture for waitlist (if not ready to launch)
- [ ] Deploy to Vercel or Netlify

**Tools**: Next.js, Tailwind CSS, or Webflow (no-code)

---

#### 6.2 App Store Optimization (ASO)
**Status**: ❌ Not Started
**Owner**: Growth Team
**Timeline**: Ongoing

**Tasks**:
- [ ] Research keywords (use App Store Connect Search Ads or Sensor Tower)
- [ ] Optimize app name and subtitle (already done in listing copy)
- [ ] A/B test screenshots (use Custom Product Pages after launch)
- [ ] Monitor conversion rate (installs ÷ page views)
- [ ] Iterate on listing copy based on data

---

#### 6.3 Launch Marketing
**Status**: ❌ Not Started
**Owner**: Marketing Team
**Timeline**: 1 week

**Tasks**:
- [ ] **Product Hunt Launch**:
  - Submit to Product Hunt (aim for #1 Product of the Day)
  - Prepare tagline, images, demo video
  - Engage with comments (founder should be active)

- [ ] **Social Media**:
  - Create Twitter/X account (@TimbuktooAI)
  - Create Instagram account (@timbuktoo.app)
  - Post launch announcement
  - Share user testimonials (once you have users)

- [ ] **Content Marketing**:
  - Write blog post: "How AI Can Plan Your Perfect Trip in 30 Seconds"
  - Submit to Hacker News, Reddit (r/travel, r/solotravel)
  - Reach out to travel bloggers for reviews

- [ ] **Paid Ads** (Optional):
  - Apple Search Ads ($500 budget)
  - Google App Campaigns ($500 budget)
  - Target keywords: "travel planner", "ai travel", "itinerary planner"

---

## Critical Path (Minimum Viable Launch)

**If you only have 4 weeks, focus on this**:

### Week 1: Backend + Database
- [ ] Set up database (PostgreSQL on AWS RDS or Supabase)
- [ ] Implement auth endpoints (signup, login)
- [ ] Implement stub endpoints (hardcoded cities, mock itineraries)
- [ ] Deploy to production (Heroku or AWS EC2)

### Week 2: Mobile App (Core Screens)
- [ ] Implement Splash, Welcome, AI Disclosure, Auth screens
- [ ] Implement Preferences screen
- [ ] Implement City Recommendation screen (hardcoded 3 cities)
- [ ] Implement Itinerary screen (mock data)

### Week 3: App Store Submission
- [ ] Create screenshots (5 for iOS, 4 for Android)
- [ ] Build production apps (EAS Build or Xcode/Android Studio)
- [ ] Submit to App Store and Google Play
- [ ] Set up crash reporting (Firebase Crashlytics)

### Week 4: Launch Prep + AI Integration
- [ ] Integrate Anthropic Claude API (replace mock data)
- [ ] Create demo account with pre-generated itinerary
- [ ] Create landing page (simple Next.js site)
- [ ] Prepare Product Hunt launch

**Launch Day** (End of Week 4):
- [ ] App approved on iOS and Android
- [ ] Product Hunt launch
- [ ] Social media announcement
- [ ] Monitor crash-free rate and user feedback

---

## Post-Launch (Week 5-8)

### Week 5: Iterate Based on Feedback
- [ ] Fix P0/P1 bugs from user feedback
- [ ] Monitor crash-free rate (target: 99%+)
- [ ] Analyze first cohort retention (D7, D30)

### Week 6: Add Payment Processing
- [ ] Set up RevenueCat + Stripe
- [ ] Implement paywall screen
- [ ] Test in-app purchases (Sandbox on iOS, License Testing on Android)
- [ ] Launch paid plans

### Week 7: Run First Experiment
- [ ] Launch Experiment 1 (Skip Preferences vs. Full Flow)
- [ ] Monitor activation rate
- [ ] Ship winning variant to 100%

### Week 8: Scale & Optimize
- [ ] Launch Experiment 2 (Paywall Timing)
- [ ] Deploy Trust Portal (trust.timbuktoo.app)
- [ ] Reach out to first enterprise prospects

---

## Key Decisions to Make Now

### 1. MVP Scope
**Question**: Launch with AI integration or hardcoded data first?

**Option A: Hardcoded Data (Faster)**
- Pros: Launch in 3-4 weeks, no AI costs, can validate UX first
- Cons: Not the real product, can't test AI quality

**Option B: AI Integration (Better)**
- Pros: Real product, can test AI quality, better user feedback
- Cons: Takes 4-6 weeks, Anthropic API costs (~$100/month for 1,000 itineraries)

**Recommendation**: Option B (AI Integration). The AI is your core value prop.

---

### 2. Payment Processing
**Question**: Launch with IAP or wait?

**Option A: Launch Free-Only**
- Pros: Faster launch, focus on UX first
- Cons: No revenue, harder to test monetization

**Option B: Launch with IAP**
- Pros: Immediate revenue, can test conversion
- Cons: Adds 1-2 weeks to timeline

**Recommendation**: Option A for MVP (launch free-only), add IAP in Week 6.

---

### 3. Backend Hosting
**Question**: Where to host backend?

**Option A: Heroku**
- Pros: Easy setup, no DevOps needed
- Cons: More expensive ($25-100/month)

**Option B: AWS EC2**
- Pros: Cheaper ($10-30/month), more control
- Cons: Requires DevOps knowledge

**Option C: Serverless (AWS Lambda + API Gateway)**
- Pros: Pay-per-use, scales automatically
- Cons: Cold starts, more complex

**Recommendation**: Option A (Heroku) for MVP, migrate to AWS later.

---

## Resource Requirements

**Team**:
- 1 Backend Engineer (FastAPI, PostgreSQL, Anthropic API)
- 1 Mobile Engineer (React Native, Expo)
- 1 Designer (screenshots, landing page)
- 1 Product Manager (App Store submission, launch coordination)

**Budget** (First 3 Months):
- Hosting: $100/month (Heroku + PostgreSQL)
- Anthropic API: $100/month (1,000 itineraries)
- Apple Developer: $99/year (one-time)
- Google Play Developer: $25 (one-time)
- Domain: $12/year
- Firebase: $0 (free tier)
- RevenueCat: $0 (free tier)
- **Total**: ~$500 for 3 months

**Timeline Summary**:
- **Fastest Path**: 4 weeks (hardcoded data, no IAP)
- **Realistic Path**: 6 weeks (AI integration, no IAP)
- **Full MVP**: 8 weeks (AI integration + IAP + experiments)

---

**Last Updated**: 2024-07-16
**Next Steps**: Prioritize Week 1 tasks (database + backend API)
