# Timbuktoo Mobile App

React Native + Expo mobile app for iOS and Android.

---

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env and set API_BASE_URL
```

### 3. Start Development Server

```bash
npm start
```

Press `i` for iOS simulator or `a` for Android emulator.

---

## Screens

1. **SplashScreen** - App startup with auth check
2. **OnboardingWelcomeScreen** - Welcome message
3. **AIDisclosureScreen** ⚠️ - CRITICAL: Mandatory AI consent (Apple Guideline 5.1.1)
4. **DataUseScreen** - Privacy Policy and data use consent
5. **AuthScreen** - Email/password login and signup
6. **PreferencesScreen** - Travel preferences (interests, budget, pace)
7. **CityRecommendationScreen** - AI-recommended cities
8. **ItineraryScreen** ⚠️ - CRITICAL: AI banner required on all itineraries
9. **FeedbackScreen** ⚠️ - CRITICAL: Report issues (Apple Guideline 5.1.1)
10. **SettingsScreen** - Privacy Policy, Delete My Data, Logout

---

## Development

```bash
# Start development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android

# Type checking
npx tsc --noEmit
```

---

## App Store Submission

See `/docs/mobile/app-store/` for:
- Screenshot requirements
- App Store listing copy
- Privacy Nutrition Label
- Reviewer demo account

---

## Environment Variables

```bash
API_BASE_URL=http://localhost:8000
```

For production:
```bash
API_BASE_URL=https://api.timbuktoo.app
```
