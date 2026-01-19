# Crash Reporting & Error Tracking Setup - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Platforms**: iOS & Android
**Recommended Tool**: Firebase Crashlytics (Primary) + Sentry (Optional for advanced features)

This guide covers the complete setup of crash reporting and error tracking for Timbuktoo Mobile, which is **REQUIRED before App Store submission**.

---

## Table of Contents

1. [Why Crash Reporting is Required](#why-crash-reporting-is-required)
2. [Tool Comparison](#tool-comparison)
3. [Firebase Crashlytics Setup (Recommended)](#firebase-crashlytics-setup-recommended)
4. [Sentry Setup (Alternative/Supplement)](#sentry-setup-alternativesupplement)
5. [Error Tracking Best Practices](#error-tracking-best-practices)
6. [App Store Compliance](#app-store-compliance)
7. [Testing & Validation](#testing--validation)

---

## Why Crash Reporting is Required

### App Store Requirements

**Apple App Store**:
- **Not technically required**, but strongly recommended
- Apple provides basic crash reports via Xcode Organizer, but they're delayed (24-48 hours)
- Real-time crash reporting helps you fix critical bugs before rejection

**Google Play Store**:
- **Not technically required**, but strongly recommended
- Google provides Android Vitals, but it's limited to post-launch metrics
- Pre-launch reports require crash-free rate > 99.5% for "Good" rating

### Production Requirements

**Critical Bugs to Catch**:
1. **App Launch Failures** - App crashes on startup (instant rejection)
2. **Authentication Errors** - JWT token failures, API 401/403 errors
3. **API Failures** - Network errors, timeout errors, 500 errors
4. **AI Generation Errors** - Claude API failures, rate limits
5. **Payment Errors** - In-app purchase failures, receipt validation errors

**Benefits**:
- **Real-time alerts** - Get notified within seconds of a crash
- **Stack traces** - See exact line of code causing crash
- **User context** - Device model, OS version, app version
- **Crash-free rate** - Track stability over time (target: 99.9%+)

---

## Tool Comparison

| Feature | Firebase Crashlytics | Sentry |
|---------|---------------------|--------|
| **Price** | Free (unlimited crashes) | Free tier: 5,000 errors/month |
| **Setup Time** | 30 minutes | 15 minutes |
| **iOS Support** | ✅ Native | ✅ Native |
| **Android Support** | ✅ Native | ✅ Native |
| **Real-time Alerts** | ✅ Slack, Email | ✅ Slack, Email, PagerDuty |
| **Stack Traces** | ✅ Symbolication | ✅ Symbolication |
| **Custom Logs** | ✅ Logs, Keys | ✅ Breadcrumbs, Context |
| **Performance Monitoring** | ✅ (separate SDK) | ✅ (same SDK) |
| **Session Replay** | ❌ | ✅ (paid) |
| **Recommendation** | **Primary** (free, reliable) | **Supplement** (advanced features) |

**Recommended Approach**: Use Firebase Crashlytics as primary crash reporter (free, reliable), add Sentry if you need advanced features like session replay or performance monitoring.

---

## Firebase Crashlytics Setup (Recommended)

### Step 1: Create Firebase Project

1. **Go to Firebase Console**: https://console.firebase.google.com
2. **Create New Project**:
   - Project name: "Timbuktoo Mobile"
   - Enable Google Analytics: Yes (recommended)
   - Select Analytics location: United States
3. **Add iOS App**:
   - iOS bundle ID: `ai.timbuktoo.mobile`
   - App nickname: "Timbuktoo iOS"
   - Download `GoogleService-Info.plist`
4. **Add Android App**:
   - Android package name: `ai.timbuktoo.mobile`
   - App nickname: "Timbuktoo Android"
   - Download `google-services.json`

### Step 2: Install Dependencies

**Install React Native Firebase**:
```bash
npm install @react-native-firebase/app @react-native-firebase/crashlytics
```

**iOS Setup**:
```bash
cd ios
pod install
cd ..
```

### Step 3: Configure iOS

**ios/Podfile** (Add Firebase SDK):
```ruby
# Already added by pod install, but verify:
pod 'Firebase/Crashlytics'
```

**Add GoogleService-Info.plist**:
1. Drag `GoogleService-Info.plist` into `ios/` folder in Xcode
2. Ensure "Copy items if needed" is checked
3. Add to target: Timbuktoo

**ios/AppDelegate.mm** (Initialize Firebase):
```objc
#import <Firebase.h>

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
  // Initialize Firebase
  [FIRApp configure];

  // ... existing code
  return YES;
}

@end
```

**Xcode Build Phase** (Upload dSYMs for symbolication):
1. Open Xcode → Project → Targets → Build Phases
2. Click "+" → New Run Script Phase
3. Add script:
```bash
"${PODS_ROOT}/FirebaseCrashlytics/run"
```
4. Add input files:
```
${DWARF_DSYM_FOLDER_PATH}/${DWARF_DSYM_FILE_NAME}/Contents/Resources/DWARF/${TARGET_NAME}
${BUILT_PRODUCTS_DIR}/${INFOPLIST_PATH}
```

### Step 4: Configure Android

**android/build.gradle** (Project-level):
```gradle
buildscript {
  dependencies {
    classpath 'com.google.gms:google-services:4.3.15'
    classpath 'com.google.firebase:firebase-crashlytics-gradle:2.9.5'
  }
}
```

**android/app/build.gradle** (App-level):
```gradle
apply plugin: 'com.android.application'
apply plugin: 'com.google.gms.google-services' // Add this
apply plugin: 'com.google.firebase.crashlytics' // Add this

dependencies {
  implementation 'com.google.firebase:firebase-crashlytics:18.3.7'
  implementation 'com.google.firebase:firebase-analytics:21.3.0'
}
```

**Add google-services.json**:
1. Copy `google-services.json` to `android/app/` directory

**android/app/src/main/AndroidManifest.xml**:
```xml
<application>
  <!-- Add Crashlytics data collection (optional, defaults to true) -->
  <meta-data
    android:name="firebase_crashlytics_collection_enabled"
    android:value="true" />
</application>
```

### Step 5: Initialize in App

**App.tsx**:
```typescript
import React, { useEffect } from 'react';
import crashlytics from '@react-native-firebase/crashlytics';

export default function App() {
  useEffect(() => {
    // Enable Crashlytics data collection
    crashlytics().setCrashlyticsCollectionEnabled(true);

    // Set user identifier (AFTER authentication)
    // crashlytics().setUserId('user-123'); // Don't call until user logs in

    // Log app version
    crashlytics().setAttribute('app_version', '1.0.0');
    crashlytics().setAttribute('platform', Platform.OS);

    // Test crash reporting (REMOVE BEFORE PRODUCTION)
    // crashlytics().crash(); // Force crash for testing
  }, []);

  return (
    // ... app code
  );
}
```

### Step 6: Add Crash Logging

**src/utils/crashReporting.ts**:
```typescript
import crashlytics from '@react-native-firebase/crashlytics';

// Log non-fatal error
export function logError(error: Error, context?: Record<string, string>) {
  console.error('Error:', error);

  // Add context attributes
  if (context) {
    Object.entries(context).forEach(([key, value]) => {
      crashlytics().setAttribute(key, value);
    });
  }

  // Record non-fatal error
  crashlytics().recordError(error);
}

// Log custom event
export function logEvent(event: string, params?: Record<string, string>) {
  crashlytics().log(`${event}: ${JSON.stringify(params)}`);
}

// Set user ID (call after login)
export function setUserId(userId: string) {
  crashlytics().setUserId(userId);
}

// Clear user ID (call after logout)
export function clearUserId() {
  crashlytics().setUserId('');
}
```

**src/api/client.ts** (Log API errors):
```typescript
import axios from 'axios';
import { logError } from '../utils/crashReporting';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Response interceptor for error logging
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log API errors to Crashlytics
    if (error.response) {
      // Server responded with error status
      logError(new Error(`API Error: ${error.response.status} ${error.config.url}`), {
        status: String(error.response.status),
        url: error.config.url,
        method: error.config.method,
      });
    } else if (error.request) {
      // Network error (no response)
      logError(new Error(`Network Error: ${error.config.url}`), {
        url: error.config.url,
        error: error.message,
      });
    } else {
      // Request setup error
      logError(error);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

**src/screens/ItineraryScreen.tsx** (Log AI generation errors):
```typescript
async function generateItinerary(cityId: string) {
  try {
    setLoading(true);
    const itinerary = await itineraryAPI.generateItinerary(token, cityId);
    setItinerary(itinerary);
  } catch (error) {
    // Log error with context
    logError(error as Error, {
      screen: 'ItineraryScreen',
      cityId: cityId,
      userId: userId,
    });

    Alert.alert('Error', 'Failed to generate itinerary. Please try again.');
  } finally {
    setLoading(false);
  }
}
```

### Step 7: Configure Alerts

1. **Firebase Console → Crashlytics → Settings**
2. **Enable Velocity Alerts**:
   - Alert me when: Crash-free rate drops below 99%
   - For version: Latest version
   - Notification: Email + Slack
3. **Add Slack Integration** (recommended):
   - Install Firebase app in Slack
   - Connect to #timbuktoo-alerts channel
   - Test with `crashlytics().crash()` (remove before production)

### Step 8: Verify Setup

**Test Crash Reporting** (iOS):
```bash
# 1. Add test crash in App.tsx
import crashlytics from '@react-native-firebase/crashlytics';

useEffect(() => {
  setTimeout(() => {
    crashlytics().crash(); // Force crash after 5 seconds
  }, 5000);
}, []);

# 2. Build and run
cd ios
xcodebuild -workspace Timbuktoo.xcworkspace -scheme Timbuktoo -configuration Release -derivedDataPath build
cd ..
npx react-native run-ios --configuration Release

# 3. App will crash after 5 seconds
# 4. Re-open app (crash reports sent on next launch)
# 5. Wait 2-3 minutes, check Firebase Console → Crashlytics
```

**Test Crash Reporting** (Android):
```bash
# 1. Same as iOS (add crashlytics().crash())
# 2. Build and run
npx react-native run-android --variant=release

# 3. App will crash, re-open
# 4. Check Firebase Console → Crashlytics
```

**IMPORTANT**: Remove `crashlytics().crash()` before production submission!

---

## Sentry Setup (Alternative/Supplement)

### Step 1: Create Sentry Project

1. **Sign up at Sentry.io**: https://sentry.io/signup/
2. **Create New Project**:
   - Platform: React Native
   - Project name: "timbuktoo-mobile"
   - Copy DSN: `https://[KEY]@o[ORG].ingest.sentry.io/[PROJECT]`

### Step 2: Install Sentry SDK

```bash
npm install @sentry/react-native
npx @sentry/wizard -i reactNative -p ios android
```

**Wizard will**:
- Add Sentry configuration to `ios/` and `android/`
- Create `sentry.properties` files
- Update build scripts for iOS and Android

### Step 3: Initialize Sentry

**App.tsx**:
```typescript
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://[KEY]@o[ORG].ingest.sentry.io/[PROJECT]',
  tracesSampleRate: 1.0, // 100% of transactions (reduce to 0.1 for production)
  environment: __DEV__ ? 'development' : 'production',
  enableAutoSessionTracking: true,
  sessionTrackingIntervalMillis: 30000, // 30 seconds
});

export default Sentry.wrap(App); // Wrap App component
```

### Step 4: Add Error Logging

**src/utils/errorReporting.ts**:
```typescript
import * as Sentry from '@sentry/react-native';

export function logError(error: Error, context?: Record<string, any>) {
  Sentry.captureException(error, {
    contexts: { custom: context },
  });
}

export function logMessage(message: string, level: 'info' | 'warning' | 'error' = 'info') {
  Sentry.captureMessage(message, level);
}

export function setUser(userId: string, email: string) {
  Sentry.setUser({ id: userId, email });
}

export function clearUser() {
  Sentry.setUser(null);
}

// Add breadcrumb (tracks user actions leading to crash)
export function addBreadcrumb(message: string, category: string, data?: Record<string, any>) {
  Sentry.addBreadcrumb({
    message,
    category,
    data,
    level: 'info',
  });
}
```

**Usage Example**:
```typescript
import { addBreadcrumb, logError } from '../utils/errorReporting';

async function handleLogin(email: string, password: string) {
  addBreadcrumb('User attempted login', 'auth', { email });

  try {
    const result = await authAPI.login(email, password);
    addBreadcrumb('Login successful', 'auth', { userId: result.userId });
  } catch (error) {
    logError(error as Error, { screen: 'AuthScreen', email });
    Alert.alert('Login Failed', 'Invalid credentials');
  }
}
```

### Step 5: Performance Monitoring (Optional)

**Track Slow API Calls**:
```typescript
import * as Sentry from '@sentry/react-native';

async function generateItinerary(cityId: string) {
  const transaction = Sentry.startTransaction({
    op: 'itinerary.generate',
    name: 'Generate Itinerary',
  });

  try {
    const itinerary = await itineraryAPI.generateItinerary(token, cityId);
    transaction.setStatus('ok');
    return itinerary;
  } catch (error) {
    transaction.setStatus('unknown_error');
    throw error;
  } finally {
    transaction.finish(); // Logs duration to Sentry
  }
}
```

---

## Error Tracking Best Practices

### What to Log

**✅ DO Log**:
1. **App Crashes** - Unhandled exceptions, fatal errors
2. **API Failures** - 500 errors, timeout errors, network failures
3. **Authentication Errors** - JWT validation failures, 401/403 errors
4. **Payment Errors** - In-app purchase failures, receipt validation errors
5. **AI Generation Errors** - Claude API failures, rate limit errors
6. **User Actions** - Login, logout, itinerary generation (breadcrumbs only)

**❌ DO NOT Log**:
1. **Passwords** - Never log plaintext passwords
2. **JWT Tokens** - Redact tokens in error logs
3. **PII** - Minimize email addresses, phone numbers
4. **Credit Card Info** - Never log payment data (Stripe handles this)

### Error Context

**Always Include**:
- **User ID** - Helps identify affected users
- **Screen Name** - Where the error occurred
- **App Version** - iOS 1.0.0 (123) or Android 1.0.0 (123)
- **Device Info** - iPhone 15 Pro, iOS 17.2 / Pixel 5, Android 13
- **Network Status** - WiFi, cellular, offline

**Example**:
```typescript
logError(error, {
  userId: userId,
  screen: 'ItineraryScreen',
  appVersion: '1.0.0',
  build: '123',
  device: Platform.OS === 'ios' ? 'iPhone 15 Pro' : 'Pixel 5',
  networkStatus: NetInfo.isConnected ? 'online' : 'offline',
});
```

### PII Redaction

**Redact Sensitive Data**:
```typescript
function sanitizeError(error: any): any {
  const sanitized = { ...error };

  // Redact JWT tokens
  if (sanitized.headers?.Authorization) {
    sanitized.headers.Authorization = '[REDACTED]';
  }

  // Redact passwords
  if (sanitized.password) {
    sanitized.password = '[REDACTED]';
  }

  // Redact email (keep domain for debugging)
  if (sanitized.email) {
    sanitized.email = sanitized.email.replace(/(.{3}).*@/, '$1***@');
  }

  return sanitized;
}

export function logError(error: Error, context?: Record<string, any>) {
  const sanitizedContext = context ? sanitizeError(context) : undefined;
  crashlytics().recordError(error, sanitizedContext);
}
```

---

## App Store Compliance

### Privacy Policy Update

Add to **Privacy Policy Mobile Addendum**:

```markdown
## Crash Reporting

**Tool**: Firebase Crashlytics

**Data Collected**:
- Crash logs (stack traces, device model, OS version)
- App version and build number
- User actions leading to crash (breadcrumbs)

**Data Shared With**:
- Google (Firebase) - Infrastructure provider, SOC-2 certified

**Retention Period**: 90 days (automatic deletion)

**PII Protection**:
- No passwords or payment data logged
- User IDs pseudonymized (hashed)
- JWT tokens redacted from logs
```

### App Store Privacy Label

**Add to iOS Privacy Nutrition Label**:

**Diagnostics** (Category):
- **Crash Data**: Yes
- **Linked to User**: No (we use pseudonymized user IDs)
- **Used for Tracking**: No
- **Purpose**: App Functionality (bug fixes)

**Add to Google Play Data Safety**:

**App info and performance** → **Crash logs**:
- Collected: Yes
- Shared with third parties: No (Firebase is service provider)
- Optional: No
- Purpose: App functionality
- Encrypted in transit: Yes
- User can request deletion: Yes (delete account deletes all data)

---

## Testing & Validation

### Pre-Submission Checklist

**Firebase Crashlytics**:
- [ ] Firebase project created
- [ ] GoogleService-Info.plist added to iOS
- [ ] google-services.json added to Android
- [ ] Crashlytics initialized in App.tsx
- [ ] Test crash sent and received in Firebase Console
- [ ] dSYM upload script added to Xcode (iOS)
- [ ] ProGuard mapping files uploaded (Android, if using R8/ProGuard)
- [ ] Velocity alerts configured (crash-free rate < 99%)
- [ ] Slack alerts configured (optional)
- [ ] All `crashlytics().crash()` test code removed

**Sentry** (if using):
- [ ] Sentry project created
- [ ] DSN configured in App.tsx
- [ ] Test error sent and received in Sentry
- [ ] User context set after login
- [ ] Breadcrumbs added for critical actions
- [ ] Performance monitoring enabled (optional)

**Privacy Compliance**:
- [ ] Privacy Policy updated with crash reporting disclosure
- [ ] iOS Privacy Nutrition Label updated
- [ ] Google Play Data Safety form updated
- [ ] PII redaction implemented (passwords, tokens)

### Test Scenarios

**Test 1: Fatal Crash**:
1. Add `throw new Error('Test crash')` in App.tsx
2. Run app, trigger crash
3. Re-open app (crash sent on next launch)
4. Verify crash appears in Firebase Console

**Test 2: API Error**:
1. Disconnect WiFi
2. Attempt to generate itinerary
3. Verify network error logged in Firebase Console

**Test 3: Authentication Error**:
1. Manually expire JWT token (change secret key on backend)
2. Attempt API call
3. Verify 401 error logged in Firebase Console

**Test 4: User Context**:
1. Log in with demo account
2. Generate itinerary
3. Check Firebase Console → Crashlytics → Users
4. Verify user ID appears in crash reports

---

## Common Issues

### Issue 1: "Crashlytics Not Receiving Crashes"
**Cause**: dSYM files not uploaded (iOS only)
**Fix**:
1. Xcode → Build Phases → Run Script (add Firebase Crashlytics script)
2. Archive build (Product → Archive)
3. Window → Organizer → Archives → Upload to App Store
4. dSYMs automatically uploaded with build

### Issue 2: "Stack Trace Not Symbolicated"
**Cause**: Missing mapping files (Android) or dSYMs (iOS)
**Fix**:
- iOS: See Issue 1
- Android: Enable ProGuard mapping upload in `android/app/build.gradle`:
```gradle
android {
  buildTypes {
    release {
      firebaseCrashlytics {
        mappingFileUploadEnabled true
      }
    }
  }
}
```

### Issue 3: "Too Many Crash Reports (Spam)"
**Cause**: Dev crashes sent to production Crashlytics
**Fix**: Disable Crashlytics in development:
```typescript
if (__DEV__) {
  crashlytics().setCrashlyticsCollectionEnabled(false);
}
```

---

## Cost Analysis

### Firebase Crashlytics
- **Free Tier**: Unlimited crashes, unlimited users
- **No paid tier** (completely free)
- **Included**: Real-time alerts, stack traces, user analytics

### Sentry
- **Free Tier**: 5,000 errors/month, 10,000 performance units/month
- **Paid Tier**: $26/month (50,000 errors/month)
- **Overage**: $0.000045 per error after limit

**Recommendation**: Use Firebase Crashlytics (free, unlimited). Add Sentry only if you need session replay or advanced performance monitoring.

---

**Last Updated**: 2024-07-16
**Next Review**: After first production release (monitor crash-free rate)
