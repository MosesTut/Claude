# TestFlight & Internal Testing Guide - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Platforms**: iOS (TestFlight) & Android (Internal Testing Track)

This guide covers the complete workflow for internal testing before App Store and Google Play submission.

---

## Table of Contents

1. [Testing Strategy](#testing-strategy)
2. [iOS - TestFlight Setup](#ios---testflight-setup)
3. [Android - Internal Testing Setup](#android---internal-testing-setup)
4. [Testing Checklist](#testing-checklist)
5. [Bug Reporting & Triage](#bug-reporting--triage)
6. [Pre-Launch Validation](#pre-launch-validation)

---

## Testing Strategy

### Testing Phases

**Phase 1: Internal Testing** (1-2 weeks)
- **Who**: Engineering team (5-10 people)
- **Goal**: Identify critical bugs, crashes, UI issues
- **Tools**: TestFlight (iOS), Internal Testing Track (Android)
- **Success Criteria**: Crash-free rate > 99%, no P0 bugs

**Phase 2: Beta Testing** (Optional, 2-4 weeks)
- **Who**: Early adopters, travel enthusiasts (50-100 people)
- **Goal**: Validate UX, AI recommendations, onboarding flow
- **Tools**: TestFlight External Testing (iOS), Closed Testing (Android)
- **Success Criteria**: 4.0+ star feedback, < 5% churn on day 7

**Phase 3: Production Launch**
- **Release**: Submit to App Store and Google Play
- **Monitoring**: Firebase Crashlytics, Analytics, User Feedback

### Recommended Timeline

| Week | Activity | Platform | Deliverable |
|------|----------|----------|-------------|
| Week 1 | Internal Testing | iOS + Android | Fix P0/P1 bugs |
| Week 2 | Internal Testing | iOS + Android | Achieve 99%+ crash-free rate |
| Week 3 | Beta Testing (optional) | iOS + Android | Gather UX feedback |
| Week 4 | App Store Submission | iOS + Android | First review |

---

## iOS - TestFlight Setup

### Prerequisites

- [ ] Apple Developer Program membership ($99/year)
- [ ] Xcode 15.0+ installed
- [ ] App Store Connect access (Admin or App Manager role)
- [ ] Code signing certificates and provisioning profiles
- [ ] Firebase Crashlytics configured

### Step 1: Configure App in App Store Connect

1. **Log in to App Store Connect**: https://appstoreconnect.apple.com
2. **Create New App**:
   - Click "My Apps" → "+" → "New App"
   - Platform: iOS
   - Name: Timbuktoo
   - Primary Language: English (U.S.)
   - Bundle ID: ai.timbuktoo.mobile (select from dropdown)
   - SKU: timbuktoo-mobile-ios (unique identifier)
   - User Access: Full Access
3. **Fill Basic Info**:
   - Privacy Policy URL: https://timbuktoo.ai/privacy
   - Category: Travel
   - Age Rating: 4+ (complete questionnaire)

### Step 2: Create Archive Build

**Open Xcode**:
1. Open `ios/Timbuktoo.xcworkspace`
2. Select target: Timbuktoo
3. Select scheme: Timbuktoo (not -tvOS)
4. Select device: Any iOS Device (arm64)

**Configure Build Settings**:
1. Signing & Capabilities:
   - Team: Your Apple Developer Team
   - Bundle Identifier: ai.timbuktoo.mobile
   - Signing: Automatic (or Manual if using specific profiles)
2. Build Configuration: Release
3. Version: 1.0.0
4. Build: 1 (increment for each upload)

**Archive**:
```bash
# Clean build folder
Product → Clean Build Folder (Cmd+Shift+K)

# Archive
Product → Archive (Cmd+B won't work, must use Archive)

# Wait 5-10 minutes for archive to complete
```

**Alternative - Command Line** (faster for CI/CD):
```bash
cd ios

# Archive
xcodebuild archive \
  -workspace Timbuktoo.xcworkspace \
  -scheme Timbuktoo \
  -configuration Release \
  -archivePath build/Timbuktoo.xcarchive \
  CODE_SIGN_IDENTITY="Apple Distribution: Your Name (TEAM_ID)" \
  PROVISIONING_PROFILE_SPECIFIER="Timbuktoo App Store Profile"

# Export IPA
xcodebuild -exportArchive \
  -archivePath build/Timbuktoo.xcarchive \
  -exportPath build \
  -exportOptionsPlist ExportOptions.plist

# Upload to App Store Connect
xcrun altool --upload-app \
  --type ios \
  --file build/Timbuktoo.ipa \
  --username "your-apple-id@example.com" \
  --password "app-specific-password"
```

**ExportOptions.plist**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
    <key>uploadBitcode</key>
    <false/>
</dict>
</plist>
```

### Step 3: Upload to TestFlight

**Via Xcode Organizer** (Recommended for first upload):
1. Window → Organizer (Cmd+Shift+Option+O)
2. Select archive from list
3. Click "Distribute App"
4. Select "App Store Connect"
5. Select "Upload"
6. Configure options:
   - Include symbols: ✅ Yes (required for crash symbolication)
   - Upload your app's symbols: ✅ Yes
   - Manage Version and Build Number: ✅ Yes (auto-increment)
7. Click "Upload"
8. Wait 5-10 minutes for processing

**Via Transporter App** (Faster for subsequent uploads):
1. Download Transporter from Mac App Store
2. Sign in with Apple ID
3. Drag Timbuktoo.ipa to Transporter
4. Click "Deliver"

### Step 4: Configure TestFlight

1. **App Store Connect → TestFlight**
2. **Wait for Processing**: "Processing" → "Ready to Submit" (10-30 minutes)
3. **Export Compliance**:
   - Click build → Export Compliance Information
   - Does your app use encryption? **No** (we use standard TLS/AES, exempt)
   - Save
4. **What to Test** (Optional):
   ```
   Welcome to Timbuktoo Mobile v1.0.0 (Build 1)!

   Please test the following:
   1. Onboarding flow (especially AI disclosure consent)
   2. Login/signup
   3. Preferences selection
   4. City recommendations
   5. Itinerary generation (30-60 seconds is expected)
   6. Feedback/reporting
   7. Settings (especially "Delete My Data")

   Known Issues:
   - None yet

   How to Report Bugs:
   - Screenshot the issue
   - Email to engineering@timbuktoo.ai with steps to reproduce
   ```
5. **Enable Testing**: Click "Start Testing" (makes build available to testers)

### Step 5: Add Internal Testers

**Internal Testing** (Up to 100 testers, no App Review required):
1. TestFlight → Internal Testing → Default Group
2. Click "+" → Add Testers
3. Enter emails (must have App Store Connect access):
   ```
   alice@timbuktoo.ai
   bob@timbuktoo.ai
   charlie@timbuktoo.ai
   ```
4. Testers receive email invitation automatically
5. Install TestFlight app from App Store
6. Tap "Install" in invitation email
7. Open Timbuktoo in TestFlight

**Tester Instructions** (Include in invitation email):
```
Hi Team,

You've been invited to test Timbuktoo Mobile v1.0.0!

SETUP:
1. Install TestFlight from App Store (if not already installed)
2. Tap "View in TestFlight" in this email
3. Install Timbuktoo
4. Launch app and complete onboarding

DEMO ACCOUNT (pre-filled with preferences):
Email: demo@timbuktoo.ai
Password: Demo123!

TEST CHECKLIST:
□ Complete onboarding (all 3 screens)
□ Log in with demo account
□ Set travel preferences
□ View city recommendations (3 cities)
□ Generate itinerary (wait 30-60 seconds)
□ View itinerary with AI banner
□ Submit feedback
□ Settings → Delete My Data (DO NOT DELETE demo account)

BUG REPORTING:
- Screenshot the issue
- Email engineering@timbuktoo.ai with:
  - Steps to reproduce
  - Expected vs actual behavior
  - Device model and iOS version

Thank you!
Engineering Team
```

### Step 6: Monitor Feedback

**TestFlight Crash Reports**:
1. App Store Connect → TestFlight → Builds → [Build] → Crash Reports
2. View crash-free rate (target: 99%+)
3. Download crash logs for debugging

**Firebase Crashlytics** (Recommended):
- Real-time crash reports (faster than TestFlight)
- Stack traces with line numbers
- User context (device, OS, app version)

**Tester Feedback**:
- TestFlight → Feedback (in-app feedback from testers)
- Email feedback to engineering@timbuktoo.ai

### Step 7: Iterate

1. **Fix P0/P1 Bugs**:
   - P0: App crashes, authentication failures, critical bugs
   - P1: UI issues, slow performance, confusing UX
2. **Increment Build Number**:
   - Xcode → General → Build: 2
3. **Create New Archive**:
   - Product → Archive
4. **Upload to TestFlight**:
   - Testers auto-notified of new build
5. **Repeat Until Stable**:
   - Target: Crash-free rate > 99%, no P0 bugs

---

## Android - Internal Testing Setup

### Prerequisites

- [ ] Google Play Console access (Admin or Release Manager role)
- [ ] Android Studio installed (or EAS Build for Expo)
- [ ] Google Play Developer account ($25 one-time fee)
- [ ] Firebase Crashlytics configured

### Step 1: Create App in Google Play Console

1. **Log in to Google Play Console**: https://play.google.com/console
2. **Create App**:
   - Click "Create app"
   - App name: Timbuktoo
   - Default language: English (United States)
   - App or game: App
   - Free or paid: Free
   - Declarations:
     - ✅ I declare this app complies with Google Play policies
     - ✅ I acknowledge that this app is subject to US export laws
3. **Fill Dashboard**:
   - Set up app → App access (all users can access all features)
   - Set up app → Ads (does not contain ads)
   - Set up app → Content rating (ESRB: Everyone, PEGI: 3)
   - Set up app → Target audience (18+, not designed for children)
   - Set up app → News app (no)
   - Set up app → COVID-19 contact tracing (no)
   - Set up app → Data safety (complete form, see Google_Play_Data_Safety.md)

### Step 2: Build AAB (Android App Bundle)

**Using EAS Build** (Recommended for Expo):
```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Configure EAS Build
eas build:configure

# Build for Android (internal testing)
eas build --platform android --profile preview

# Download AAB
eas build:download --platform android
```

**Using Android Studio**:
1. Open `android/` in Android Studio
2. Build → Generate Signed Bundle / APK
3. Select "Android App Bundle"
4. Create keystore:
   - Key store path: `timbuktoo-release.keystore`
   - Password: [STORE SECURELY]
   - Key alias: timbuktoo-key
   - Key password: [STORE SECURELY]
5. Build variant: Release
6. Click "Finish"
7. AAB saved to: `android/app/release/app-release.aab`

**Using Gradle** (Command line):
```bash
cd android

# Generate signed AAB
./gradlew bundleRelease

# AAB location: app/build/outputs/bundle/release/app-release.aab
```

**android/app/build.gradle** (Configure signing):
```gradle
android {
  signingConfigs {
    release {
      storeFile file('timbuktoo-release.keystore')
      storePassword System.getenv('KEYSTORE_PASSWORD')
      keyAlias 'timbuktoo-key'
      keyPassword System.getenv('KEY_PASSWORD')
    }
  }

  buildTypes {
    release {
      signingConfig signingConfigs.release
      minifyEnabled true
      proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
  }
}
```

**IMPORTANT**: Store keystore and passwords securely! Losing the keystore means you can never update the app.

### Step 3: Upload to Internal Testing Track

1. **Google Play Console → Release → Testing → Internal testing**
2. **Create New Release**:
   - Click "Create new release"
   - Upload AAB: Drag `app-release.aab` to upload box
   - Release name: 1.0.0 (1) (auto-filled from versionName + versionCode)
   - Release notes:
     ```
     Welcome to Timbuktoo Mobile v1.0.0!

     Test Focus:
     - Onboarding flow (AI disclosure)
     - Login/signup
     - Itinerary generation (30-60 seconds expected)
     - Feedback/reporting
     - Data deletion

     Known Issues:
     - None

     Report Bugs:
     Email engineering@timbuktoo.ai with steps to reproduce
     ```
3. **Review Release**:
   - Click "Review release"
   - Check warnings (should be 0)
4. **Start Rollout to Internal Testing**:
   - Click "Start rollout to Internal testing"
   - Confirm

### Step 4: Add Internal Testers

1. **Internal Testing → Testers Tab**
2. **Create Email List**:
   - Click "Create email list"
   - List name: "Timbuktoo Internal Testers"
   - Add emails:
     ```
     alice@timbuktoo.ai
     bob@timbuktoo.ai
     charlie@timbuktoo.ai
     ```
   - Save
3. **Copy Opt-In URL**:
   - Copy URL: `https://play.google.com/apps/internaltest/[ID]`
4. **Send to Testers**:
   ```
   Hi Team,

   You've been invited to test Timbuktoo Mobile v1.0.0 on Android!

   SETUP:
   1. Open this link on your Android device: https://play.google.com/apps/internaltest/[ID]
   2. Tap "Become a tester"
   3. Tap "Download it on Google Play"
   4. Install app
   5. Launch and complete onboarding

   DEMO ACCOUNT:
   Email: demo@timbuktoo.ai
   Password: Demo123!

   TEST CHECKLIST:
   Same as iOS (see TestFlight instructions)

   BUG REPORTING:
   Email engineering@timbuktoo.ai with screenshot + steps to reproduce

   Thank you!
   Engineering Team
   ```

**Minimum Testing Period**: 14 days (Google Play requirement)
- Internal testing must run for at least 14 days before production release
- At least 20 testers must opt-in (Google recommendation)

### Step 5: Monitor Pre-Launch Report

**Google Play Console → Release → Testing → Pre-launch report**:
- **Automatic Testing**: Google tests app on 30+ devices
- **Crashes**: View crash logs
- **Screenshots**: Automated screenshots on different devices
- **Accessibility**: Accessibility issues detected
- **Security**: Security vulnerabilities (e.g., cleartext traffic)

**Fix Critical Issues**:
1. Download pre-launch report
2. Fix crashes and security issues
3. Build new AAB (increment versionCode)
4. Upload to internal testing
5. Wait for new pre-launch report (24 hours)

### Step 6: Review Feedback

**Crash Reports**:
- Google Play Console → Quality → Android vitals → Crashes
- View crash-free rate (target: 99.5%+)

**Firebase Crashlytics** (Recommended):
- Real-time crash reports
- Faster than Google Play vitals

**Tester Feedback**:
- Email feedback to engineering@timbuktoo.ai
- Google Play Console → Testing → Internal testing → Feedback (limited)

### Step 7: Iterate

1. Fix P0/P1 bugs
2. Increment versionCode in `android/app/build.gradle`:
   ```gradle
   android {
     defaultConfig {
       versionCode 2 // Increment
       versionName "1.0.0"
     }
   }
   ```
3. Build new AAB
4. Upload to internal testing
5. Repeat until stable (crash-free rate > 99.5%)

---

## Testing Checklist

### Functional Testing

**Onboarding**:
- [ ] Launch screen displays for 2 seconds
- [ ] Onboarding screens 1-3 display correctly
- [ ] AI disclosure checkbox blocks progress when unchecked
- [ ] Data use screen displays correctly
- [ ] "Skip" button on onboarding (if applicable) works

**Authentication**:
- [ ] Signup with email + password works
- [ ] Login with existing account works
- [ ] Invalid credentials show error message
- [ ] JWT token stored securely (Keychain/Keystore)
- [ ] Logout clears token

**Preferences**:
- [ ] All 8 interest categories display
- [ ] Multi-select interests works
- [ ] Food preferences (4 options) work
- [ ] Budget slider works (Low, Medium, High, Luxury)
- [ ] Optional dates picker works
- [ ] Save preferences → API call succeeds

**City Recommendations**:
- [ ] 3 cities display with reasoning
- [ ] Tap city → navigate to itinerary generation
- [ ] Loading state displays during API call

**Itinerary Generation**:
- [ ] Loading screen displays "Generating itinerary..."
- [ ] Progress indicator shows (30-60 seconds)
- [ ] Itinerary displays with AI banner
- [ ] Day-by-day format displays correctly
- [ ] Meals (breakfast, lunch, dinner) display with $$ indicators
- [ ] Activities display with descriptions
- [ ] Weather context displays

**Feedback**:
- [ ] "Give Feedback" button works
- [ ] Rating (helpful/not helpful) works
- [ ] Report issue (4 types) works
- [ ] Comments field works
- [ ] Submit feedback → success message

**Settings**:
- [ ] Privacy Policy link opens in browser
- [ ] Terms of Service link opens in browser
- [ ] Delete My Data → confirmation dialog
- [ ] Delete account → all data deleted (verify in database)
- [ ] Logout works

### Non-Functional Testing

**Performance**:
- [ ] App launch < 3 seconds
- [ ] Screen transitions smooth (60fps)
- [ ] API calls < 5 seconds (except itinerary generation)
- [ ] Itinerary generation 30-60 seconds (acceptable)
- [ ] No memory leaks (check Xcode Instruments)

**Network**:
- [ ] Works on WiFi
- [ ] Works on cellular (4G/5G)
- [ ] Offline mode shows error message
- [ ] Network timeout shows error message (30 seconds)

**Security**:
- [ ] JWT token stored in Keychain (iOS) or Keystore (Android)
- [ ] HTTPS used for all API calls
- [ ] No plaintext passwords in logs
- [ ] No JWT tokens in error logs

**Accessibility**:
- [ ] VoiceOver (iOS) reads all buttons and text
- [ ] TalkBack (Android) reads all buttons and text
- [ ] Dynamic Type (iOS) works (text scales with system settings)
- [ ] Font Scaling (Android) works

**Localization** (if applicable):
- [ ] Spanish translations work
- [ ] French translations work
- [ ] Currency symbols display correctly

### Device Testing

**iOS Devices** (Minimum):
- [ ] iPhone SE (2nd gen) - iOS 15.0 (minimum supported version)
- [ ] iPhone 13 - iOS 16
- [ ] iPhone 15 Pro - iOS 17 (latest)
- [ ] iPad Air - iPadOS 16 (if supporting iPad)

**Android Devices** (Minimum):
- [ ] Pixel 5 - Android 11 (minimum supported version)
- [ ] Samsung Galaxy S21 - Android 12
- [ ] Pixel 8 - Android 14 (latest)
- [ ] Tablet - Android 12+ (if supporting tablets)

### Edge Cases

- [ ] First launch (no account)
- [ ] Returning user (has account, skip onboarding)
- [ ] Free tier limit reached (3 itineraries/month)
- [ ] Pro subscriber (unlimited itineraries)
- [ ] Expired JWT token (re-login)
- [ ] API 500 error (retry with exponential backoff)
- [ ] Slow network (show loading state)
- [ ] App backgrounded during itinerary generation (resume on foreground)

---

## Bug Reporting & Triage

### Bug Template

**Title**: [Component] Brief description (e.g., "Onboarding: AI disclosure checkbox not blocking")

**Description**:
```
Steps to Reproduce:
1. Launch app
2. Tap "Get Started" on onboarding screen 1
3. Tap "Continue" on AI disclosure screen WITHOUT checking checkbox
4. Expected: Alert "Please confirm..." displayed
5. Actual: User navigated to next screen

Expected Behavior:
User should not be able to proceed without checking AI disclosure checkbox

Actual Behavior:
User can proceed without checking checkbox

Environment:
- Device: iPhone 15 Pro
- iOS Version: 17.2
- App Version: 1.0.0 (Build 1)
- Network: WiFi

Screenshots:
[Attach screenshot]

Crash Log:
[Attach if applicable]
```

### Bug Severity

**P0 (Critical - Fix Immediately)**:
- App crashes on launch
- Authentication completely broken
- Data loss or corruption
- Security vulnerability

**P1 (High - Fix Before Production)**:
- Feature completely broken (e.g., can't generate itinerary)
- Major UI bug (e.g., text unreadable)
- Performance issue (e.g., app freezes)

**P2 (Medium - Fix Soon)**:
- Minor UI bug (e.g., button alignment)
- Edge case error (e.g., slow network timeout)
- Non-critical feature broken (e.g., feedback submission)

**P3 (Low - Fix Later)**:
- Cosmetic issue (e.g., color mismatch)
- Feature request
- Optimization

### Bug Triage Process

1. **Report Bug**: Tester emails engineering@timbuktoo.ai or files Jira ticket
2. **Triage**: Engineering lead assigns severity (P0-P3)
3. **Assign**: Assign to developer
4. **Fix**: Developer fixes bug, creates new build
5. **Verify**: Tester verifies fix in new build
6. **Close**: Mark as resolved

---

## Pre-Launch Validation

### Final Checklist (Before Submitting to Production)

**Code Quality**:
- [ ] No `console.log()` or `console.error()` in production code
- [ ] No test crash code (`crashlytics().crash()`)
- [ ] No hardcoded API keys or secrets
- [ ] All `TODO` comments resolved
- [ ] Code reviewed by at least one other developer

**Testing**:
- [ ] Crash-free rate > 99% (iOS) or 99.5% (Android)
- [ ] All P0 bugs fixed
- [ ] All P1 bugs fixed
- [ ] TestFlight tested on 5+ devices
- [ ] Internal testing tested on 20+ devices (Android)

**Compliance**:
- [ ] Privacy Policy URL valid and accessible
- [ ] Terms of Service URL valid and accessible
- [ ] AI disclosure checkbox on onboarding
- [ ] AI banner on every itinerary
- [ ] Feedback/report mechanism on every itinerary
- [ ] Delete My Data in Settings
- [ ] Restore Purchases in Settings (if IAP enabled)

**App Store Assets**:
- [ ] App icon (1024x1024 PNG, no transparency)
- [ ] Screenshots (5 for iOS, 4-6 for Android)
- [ ] App Store listing copy complete
- [ ] Google Play Store listing copy complete
- [ ] App Review Notes complete
- [ ] Privacy Nutrition Label declared (iOS)
- [ ] Data Safety form complete (Android)

**Backend**:
- [ ] Production API deployed (https://api.timbuktoo.ai)
- [ ] Database migrations run
- [ ] Rate limiting enabled
- [ ] Monitoring enabled (Datadog, Firebase Crashlytics)
- [ ] Backups enabled (daily snapshots)

**Infrastructure**:
- [ ] SSL certificate valid (TLS 1.2+)
- [ ] CDN configured (CloudFront)
- [ ] Load balancer healthy (2+ instances)
- [ ] Auto-scaling enabled

---

## Production Release

### iOS - Submit for Review

1. **App Store Connect → App Store → iOS App → 1.0 Prepare for Submission**
2. **Fill Required Info**:
   - Screenshots (5 required, 6.7" display)
   - Description (see iOS_App_Store_Listing.md)
   - Keywords
   - Support URL: https://timbuktoo.ai/support
   - Marketing URL: https://timbuktoo.ai
3. **Select Build**: Choose TestFlight build
4. **Version Information**:
   - Copyright: 2024 Timbuktoo Inc.
   - Age Rating: 4+
   - Sign-In Required: Yes (demo account in App Review Notes)
5. **App Review Information**:
   - Contact: support@timbuktoo.ai
   - Demo Account: reviewer@timbuktoo.ai / ReviewTest2024!
   - Notes: See App_Review_Notes.txt
6. **Submit for Review**
7. **Wait 24-72 hours** for review

### Android - Promote to Production

1. **Google Play Console → Release → Testing → Internal testing**
2. **Promote to Production**:
   - Click "Promote release" → "Production"
   - Review release details
   - Click "Start rollout to Production"
3. **Rollout Options**:
   - Staged rollout: 10% → 50% → 100% (recommended)
   - Full rollout: 100% immediately
4. **Wait 24-48 hours** for review

---

**Last Updated**: 2024-07-16
**Next Steps**: Complete internal testing, fix P0/P1 bugs, submit to production
