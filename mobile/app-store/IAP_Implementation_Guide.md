# In-App Purchase (IAP) Implementation Guide - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Platforms**: iOS (StoreKit 2) & Android (Google Play Billing Library 5.0+)

This guide covers the complete implementation of in-app purchases for Timbuktoo Mobile, including free tier limitations, subscription management, and App Store compliance.

---

## Table of Contents

1. [Monetization Model](#monetization-model)
2. [Product Configuration](#product-configuration)
3. [iOS Implementation (StoreKit 2)](#ios-implementation-storekit-2)
4. [Android Implementation (Google Play Billing)](#android-implementation-google-play-billing)
5. [Backend Subscription Management](#backend-subscription-management)
6. [UI/UX Implementation](#uiux-implementation)
7. [Testing](#testing)
8. [App Store Compliance](#app-store-compliance)

---

## Monetization Model

### Free Tier
- **Itineraries**: 3 per month
- **Features**: All core features (AI recommendations, feedback, settings)
- **Limitations**: Counter resets on 1st of each month
- **Upgrade CTA**: Shown when limit reached

### Pro Monthly
- **Price**: $9.99/month
- **Itineraries**: Unlimited
- **Features**: All features + priority support
- **Auto-Renewal**: Yes (cancel anytime)
- **Trial**: Optional 7-day free trial (configure in App Store Connect)

### Pro Annual
- **Price**: $79.99/year (33% savings vs monthly)
- **Itineraries**: Unlimited
- **Features**: All features + priority support
- **Auto-Renewal**: Yes (cancel anytime)
- **Trial**: Optional 7-day free trial

---

## Product Configuration

### iOS - App Store Connect

1. **Navigate to App Store Connect**:
   - My Apps → Timbuktoo → Features → In-App Purchases

2. **Create Auto-Renewable Subscriptions**:

**Product 1: Pro Monthly**
- **Reference Name**: Timbuktoo Pro Monthly
- **Product ID**: `ai.timbuktoo.mobile.pro.monthly`
- **Subscription Group**: `timbuktoo_pro`
- **Subscription Duration**: 1 month
- **Price**: $9.99 USD (Tier 10)
- **Localized Display Name**: "Pro Monthly"
- **Localized Description**: "Unlimited AI-generated itineraries, priority support, and all features."

**Product 2: Pro Annual**
- **Reference Name**: Timbuktoo Pro Annual
- **Product ID**: `ai.timbuktoo.mobile.pro.annual`
- **Subscription Group**: `timbuktoo_pro`
- **Subscription Duration**: 1 year
- **Price**: $79.99 USD (Tier 80)
- **Localized Display Name**: "Pro Annual"
- **Localized Description**: "Save 33%! Unlimited AI-generated itineraries, priority support, and all features for one year."

3. **Configure Subscription Group**:
   - **Name**: Timbuktoo Pro
   - **Ranking**: Pro Annual (Rank 1), Pro Monthly (Rank 2)
   - **Why**: Apple recommends annual plan first

4. **Add Introductory Offer** (Optional but Recommended):
   - **Type**: Free Trial
   - **Duration**: 7 days
   - **Availability**: New subscribers only
   - **Eligibility**: One per user, ever (Apple's default)

5. **Review Information**:
   - **Screenshot**: Upload screenshot of Pro features (Settings → Subscription screen)
   - **Review Notes**: "Pro subscription unlocks unlimited itinerary generation. Free tier allows 3 itineraries/month."

6. **Submit for Review**:
   - Submit with app binary (auto-approved with app)

### Android - Google Play Console

1. **Navigate to Google Play Console**:
   - All apps → Timbuktoo → Monetize → Subscriptions

2. **Create Subscription Products**:

**Product 1: Pro Monthly**
- **Product ID**: `pro_monthly`
- **Name**: Timbuktoo Pro Monthly
- **Description**: "Unlimited AI-generated itineraries and priority support"
- **Billing Period**: Monthly (every 1 month)
- **Price**: $9.99 USD (auto-converted to local currencies)
- **Free Trial**: 7 days (optional)
- **Grace Period**: 3 days (recommended - allows users to fix payment issues)

**Product 2: Pro Annual**
- **Product ID**: `pro_annual`
- **Name**: Timbuktoo Pro Annual
- **Description**: "Save 33%! Unlimited itineraries for one year"
- **Billing Period**: Yearly (every 1 year)
- **Price**: $79.99 USD
- **Free Trial**: 7 days (optional)
- **Grace Period**: 7 days

3. **Configure Base Plans**:
   - Enable "Backwards Compatible" for Play Billing Library 5.0+
   - Set renewal type: Auto-renewing

4. **Submit for Review**:
   - Products auto-approved (usually within 24 hours)

---

## iOS Implementation (StoreKit 2)

### Dependencies

**package.json**:
```json
{
  "dependencies": {
    "react-native-purchases": "^6.0.0"
  }
}
```

**Why RevenueCat (react-native-purchases)**:
- Unified API for iOS + Android
- Built-in receipt validation
- Free tier supports unlimited MAU (Monthly Active Users)
- Automatic subscription status sync
- Paywalls and A/B testing (optional)

**Alternative**: Use native `@react-native-community/in-app-purchases`, but RevenueCat is strongly recommended for production.

### Installation

```bash
npm install react-native-purchases
cd ios && pod install && cd ..
```

### Configuration

**App.tsx** (Initialize RevenueCat):
```typescript
import React, { useEffect } from 'react';
import Purchases from 'react-native-purchases';

export default function App() {
  useEffect(() => {
    async function initializePurchases() {
      if (Platform.OS === 'ios') {
        await Purchases.configure({ apiKey: 'appl_YOUR_REVENUECAT_API_KEY' });
      } else if (Platform.OS === 'android') {
        await Purchases.configure({ apiKey: 'goog_YOUR_REVENUECAT_API_KEY' });
      }

      // Get user subscription status
      const customerInfo = await Purchases.getCustomerInfo();
      console.log('Subscription status:', customerInfo.entitlements.active);
    }

    initializePurchases();
  }, []);

  return (
    // ... app code
  );
}
```

**Get API Keys**:
1. Sign up at https://www.revenuecat.com (free tier)
2. Create project "Timbuktoo Mobile"
3. Add iOS app (Bundle ID: `ai.timbuktoo.mobile`)
4. Add Android app (Package: `ai.timbuktoo.mobile`)
5. Copy API keys to environment variables

### Subscription Management

**src/utils/subscriptions.ts**:
```typescript
import Purchases, { PurchasesPackage } from 'react-native-purchases';

export type SubscriptionStatus = 'free' | 'pro_monthly' | 'pro_annual';

// Check if user is subscribed to Pro
export async function isProSubscriber(): Promise<boolean> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return customerInfo.entitlements.active['pro'] !== undefined;
  } catch (error) {
    console.error('Error checking subscription:', error);
    return false;
  }
}

// Get subscription status
export async function getSubscriptionStatus(): Promise<SubscriptionStatus> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();

    if (customerInfo.entitlements.active['pro']?.productIdentifier === 'ai.timbuktoo.mobile.pro.annual') {
      return 'pro_annual';
    } else if (customerInfo.entitlements.active['pro']?.productIdentifier === 'ai.timbuktoo.mobile.pro.monthly') {
      return 'pro_monthly';
    } else {
      return 'free';
    }
  } catch (error) {
    console.error('Error getting subscription status:', error);
    return 'free';
  }
}

// Get available subscription packages
export async function getSubscriptionPackages(): Promise<PurchasesPackage[]> {
  try {
    const offerings = await Purchases.getOfferings();
    if (offerings.current && offerings.current.availablePackages.length > 0) {
      return offerings.current.availablePackages;
    }
    return [];
  } catch (error) {
    console.error('Error fetching offerings:', error);
    return [];
  }
}

// Purchase a subscription
export async function purchaseSubscription(packageToPurchase: PurchasesPackage): Promise<boolean> {
  try {
    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);

    // Check if purchase was successful
    if (customerInfo.entitlements.active['pro']) {
      return true;
    }
    return false;
  } catch (error: any) {
    if (error.userCancelled) {
      console.log('User cancelled purchase');
    } else {
      console.error('Purchase error:', error);
    }
    return false;
  }
}

// Restore purchases (required by Apple)
export async function restorePurchases(): Promise<boolean> {
  try {
    const customerInfo = await Purchases.restorePurchases();
    return customerInfo.entitlements.active['pro'] !== undefined;
  } catch (error) {
    console.error('Restore error:', error);
    return false;
  }
}

// Get itinerary usage for free tier
export async function getItineraryUsage(userId: string): Promise<{ used: number; limit: number }> {
  try {
    const response = await axios.get(`${API_BASE_URL}/user/itinerary-usage`, {
      headers: { Authorization: `Bearer ${await getAuthToken()}` }
    });
    return response.data; // { used: 2, limit: 3 }
  } catch (error) {
    console.error('Error fetching usage:', error);
    return { used: 0, limit: 3 };
  }
}
```

---

## Android Implementation (Google Play Billing)

**Android-Specific Configuration**:

RevenueCat handles Android automatically, but ensure the following:

**android/app/build.gradle**:
```gradle
dependencies {
    implementation 'com.android.billingclient:billing:5.0.0'
}
```

**AndroidManifest.xml**:
```xml
<uses-permission android:name="com.android.vending.BILLING" />
```

**Google Play Console**:
- Enable "In-app products" in Monetize → Products
- Link subscription products to app

---

## Backend Subscription Management

### Database Schema

**PostgreSQL - subscriptions table**:
```sql
CREATE TABLE subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    platform VARCHAR(10) NOT NULL, -- 'ios' or 'android'
    product_id VARCHAR(100) NOT NULL, -- 'ai.timbuktoo.mobile.pro.monthly'
    status VARCHAR(20) NOT NULL, -- 'active', 'expired', 'cancelled', 'grace_period'
    starts_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    receipt_data TEXT, -- Store receipt for validation
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);

CREATE TABLE itinerary_usage (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    month VARCHAR(7) NOT NULL, -- 'YYYY-MM' (e.g., '2024-07')
    count INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Backend Endpoints

**timbuktoo/api/subscription_endpoints.py**:
```python
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/subscriptions", tags=["subscriptions"])

@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get user's current subscription status.
    Returns: { tier: 'free' | 'pro_monthly' | 'pro_annual', expiresAt: '2024-08-16', autoRenew: true }
    """
    user_id = get_user_id_from_token(credentials.credentials)

    # Check active subscription
    subscription = await db.subscriptions.find_one({
        "user_id": user_id,
        "status": "active",
        "expires_at": {"$gte": datetime.utcnow()}
    })

    if subscription:
        return SubscriptionStatusResponse(
            tier='pro_annual' if 'annual' in subscription['product_id'] else 'pro_monthly',
            expiresAt=subscription['expires_at'].isoformat(),
            autoRenew=subscription['auto_renew']
        )
    else:
        return SubscriptionStatusResponse(tier='free', expiresAt=None, autoRenew=False)

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def subscription_webhook(request: Request):
    """
    Webhook for RevenueCat to notify subscription changes.
    CRITICAL: This endpoint must be publicly accessible and secured with RevenueCat auth.
    """
    # Verify RevenueCat signature
    signature = request.headers.get('X-Revenuecat-Signature')
    if not verify_revenuecat_signature(await request.body(), signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = await request.json()

    # Handle different event types
    if event['type'] == 'INITIAL_PURCHASE':
        await handle_initial_purchase(event)
    elif event['type'] == 'RENEWAL':
        await handle_renewal(event)
    elif event['type'] == 'CANCELLATION':
        await handle_cancellation(event)
    elif event['type'] == 'EXPIRATION':
        await handle_expiration(event)

    return {"status": "ok"}

async def handle_initial_purchase(event):
    """Update database when user subscribes."""
    user_id = event['app_user_id']
    product_id = event['product_id']
    expires_at = datetime.fromisoformat(event['expires_date'])

    await db.subscriptions.insert_one({
        "user_id": user_id,
        "platform": event['store'],
        "product_id": product_id,
        "status": "active",
        "starts_at": datetime.utcnow(),
        "expires_at": expires_at,
        "auto_renew": True,
        "receipt_data": event['original_transaction_id']
    })

async def handle_cancellation(event):
    """Mark subscription as cancelled (but still active until expiration)."""
    user_id = event['app_user_id']

    await db.subscriptions.update_one(
        {"user_id": user_id, "status": "active"},
        {"$set": {"auto_renew": False, "updated_at": datetime.utcnow()}}
    )

@router.get("/usage", response_model=UsageResponse)
async def get_itinerary_usage(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get itinerary usage for free tier users.
    Returns: { used: 2, limit: 3, resetsAt: '2024-08-01T00:00:00Z' }
    """
    user_id = get_user_id_from_token(credentials.credentials)

    # Check if Pro subscriber (unlimited)
    subscription = await db.subscriptions.find_one({
        "user_id": user_id,
        "status": "active",
        "expires_at": {"$gte": datetime.utcnow()}
    })

    if subscription:
        return UsageResponse(used=0, limit=-1, resetsAt=None)  # -1 = unlimited

    # Free tier: Get usage for current month
    current_month = datetime.utcnow().strftime('%Y-%m')
    usage = await db.itinerary_usage.find_one({"user_id": user_id, "month": current_month})

    used = usage['count'] if usage else 0
    limit = 3
    resets_at = (datetime.utcnow().replace(day=1) + timedelta(days=32)).replace(day=1)

    return UsageResponse(used=used, limit=limit, resetsAt=resets_at.isoformat())

@router.post("/increment-usage", status_code=status.HTTP_204_NO_CONTENT)
async def increment_itinerary_usage(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Increment itinerary usage for free tier users.
    Called when user generates an itinerary.
    """
    user_id = get_user_id_from_token(credentials.credentials)

    # Check if Pro subscriber (no limit)
    subscription = await db.subscriptions.find_one({
        "user_id": user_id,
        "status": "active",
        "expires_at": {"$gte": datetime.utcnow()}
    })

    if subscription:
        return  # No usage tracking for Pro users

    # Increment usage for current month
    current_month = datetime.utcnow().strftime('%Y-%m')

    await db.itinerary_usage.update_one(
        {"user_id": user_id, "month": current_month},
        {"$inc": {"count": 1}, "$set": {"updated_at": datetime.utcnow()}},
        upsert=True
    )
```

**RevenueCat Webhook Configuration**:
1. Go to RevenueCat Dashboard → Integrations → Webhooks
2. Add webhook URL: `https://api.timbuktoo.ai/api/v1/subscriptions/webhook`
3. Select events: Initial Purchase, Renewal, Cancellation, Expiration
4. Copy webhook secret (used to verify signature)

---

## UI/UX Implementation

### Paywall Screen

**src/screens/PaywallScreen.tsx**:
```typescript
import React, { useState, useEffect } from 'react';
import { SafeAreaView, ScrollView, View, Text, StyleSheet, Alert } from 'react-native';
import { Button, Card, ActivityIndicator } from 'react-native-paper';
import { PurchasesPackage } from 'react-native-purchases';
import { getSubscriptionPackages, purchaseSubscription, getItineraryUsage } from '../utils/subscriptions';

export default function PaywallScreen({ navigation, route }) {
  const { source } = route.params; // 'limit_reached', 'settings', 'onboarding'
  const [packages, setPackages] = useState<PurchasesPackage[]>([]);
  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState(false);
  const [usage, setUsage] = useState({ used: 0, limit: 3 });

  useEffect(() => {
    loadPackages();
    loadUsage();
  }, []);

  async function loadPackages() {
    const pkgs = await getSubscriptionPackages();
    setPackages(pkgs);
    setLoading(false);
  }

  async function loadUsage() {
    const usageData = await getItineraryUsage();
    setUsage(usageData);
  }

  async function handlePurchase(pkg: PurchasesPackage) {
    setPurchasing(true);
    const success = await purchaseSubscription(pkg);
    setPurchasing(false);

    if (success) {
      Alert.alert(
        'Welcome to Pro!',
        'You now have unlimited itinerary generation.',
        [{ text: 'Start Exploring', onPress: () => navigation.goBack() }]
      );
    } else {
      Alert.alert('Purchase Failed', 'Please try again or contact support.');
    }
  }

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Upgrade to Timbuktoo Pro</Text>
          {source === 'limit_reached' && (
            <Text style={styles.subtitle}>
              You've used {usage.used} of {usage.limit} free itineraries this month.
            </Text>
          )}
        </View>

        {/* Features */}
        <View style={styles.features}>
          <Text style={styles.featureTitle}>Pro Features:</Text>
          <View style={styles.featureItem}>
            <Text style={styles.featureIcon}>✓</Text>
            <Text style={styles.featureText}>Unlimited AI-generated itineraries</Text>
          </View>
          <View style={styles.featureItem}>
            <Text style={styles.featureIcon}>✓</Text>
            <Text style={styles.featureText}>Priority support</Text>
          </View>
          <View style={styles.featureItem}>
            <Text style={styles.featureIcon}>✓</Text>
            <Text style={styles.featureText}>All features included</Text>
          </View>
        </View>

        {/* Subscription Cards */}
        {packages.map((pkg) => {
          const isAnnual = pkg.product.identifier.includes('annual');
          return (
            <Card key={pkg.identifier} style={styles.planCard}>
              {isAnnual && (
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>BEST VALUE - Save 33%</Text>
                </View>
              )}
              <Card.Content>
                <Text style={styles.planName}>
                  {isAnnual ? 'Pro Annual' : 'Pro Monthly'}
                </Text>
                <Text style={styles.planPrice}>
                  {pkg.product.priceString}
                  {isAnnual ? '/year' : '/month'}
                </Text>
                {isAnnual && (
                  <Text style={styles.planSavings}>Just $6.67/month</Text>
                )}
                <Button
                  mode="contained"
                  onPress={() => handlePurchase(pkg)}
                  disabled={purchasing}
                  style={styles.purchaseButton}
                >
                  {purchasing ? 'Processing...' : `Subscribe Now`}
                </Button>
              </Card.Content>
            </Card>
          );
        })}

        {/* Legal Disclaimer (REQUIRED by Apple) */}
        <Text style={styles.legalText}>
          Payment will be charged to your Apple ID account at confirmation of purchase.
          Subscription automatically renews unless canceled at least 24 hours before the
          end of the current period. Your account will be charged for renewal within 24
          hours prior to the end of the current period. You can manage and cancel
          subscriptions in your App Store account settings.
        </Text>

        {/* Links */}
        <View style={styles.links}>
          <Button onPress={() => navigation.navigate('Terms')} mode="text">
            Terms of Service
          </Button>
          <Button onPress={() => navigation.navigate('Privacy')} mode="text">
            Privacy Policy
          </Button>
        </View>

        {/* Skip Option (if not from limit_reached) */}
        {source !== 'limit_reached' && (
          <Button onPress={() => navigation.goBack()} mode="text">
            Maybe Later
          </Button>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  scrollContent: { padding: 20 },
  header: { marginBottom: 20, alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
  subtitle: { fontSize: 16, color: '#666', textAlign: 'center' },
  features: { marginBottom: 20 },
  featureTitle: { fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  featureItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  featureIcon: { fontSize: 20, color: '#4CAF50', marginRight: 10 },
  featureText: { fontSize: 16, color: '#333' },
  planCard: { marginBottom: 15, position: 'relative' },
  badge: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: '#FF9800',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 5,
    zIndex: 1,
  },
  badgeText: { fontSize: 12, fontWeight: 'bold', color: '#fff' },
  planName: { fontSize: 20, fontWeight: 'bold', marginBottom: 5 },
  planPrice: { fontSize: 18, color: '#333', marginBottom: 5 },
  planSavings: { fontSize: 14, color: '#4CAF50', marginBottom: 15 },
  purchaseButton: { marginTop: 10 },
  legalText: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 10,
    lineHeight: 18,
  },
  links: { flexDirection: 'row', justifyContent: 'center', marginTop: 10 },
});
```

### Settings - Manage Subscription

**src/screens/SettingsScreen.tsx** (Add Subscription Section):
```typescript
{/* Subscription Section */}
<View style={styles.section}>
  <Text style={styles.sectionTitle}>Subscription</Text>

  {subscriptionStatus.tier === 'free' ? (
    <>
      <Text style={styles.usageText}>
        Free Tier: {usage.used} of {usage.limit} itineraries used this month
      </Text>
      <Button mode="contained" onPress={() => navigation.navigate('Paywall', { source: 'settings' })}>
        Upgrade to Pro
      </Button>
    </>
  ) : (
    <>
      <Text style={styles.proStatus}>
        ✓ Pro {subscriptionStatus.tier === 'pro_annual' ? 'Annual' : 'Monthly'}
      </Text>
      <Text style={styles.expiresText}>
        {subscriptionStatus.autoRenew ? 'Renews' : 'Expires'} on{' '}
        {new Date(subscriptionStatus.expiresAt).toLocaleDateString()}
      </Text>
      <Button
        mode="outlined"
        onPress={() => Linking.openURL('https://apps.apple.com/account/subscriptions')}
      >
        Manage Subscription
      </Button>
    </>
  )}

  <Button mode="text" onPress={handleRestorePurchases}>
    Restore Purchases
  </Button>
</View>
```

### Itinerary Generation - Check Limit

**src/screens/CityRecommendationScreen.tsx** (Before generating itinerary):
```typescript
async function handleGenerateItinerary(cityId: string) {
  // Check subscription status
  const isPro = await isProSubscriber();

  if (!isPro) {
    // Check free tier limit
    const usage = await getItineraryUsage();

    if (usage.used >= usage.limit) {
      // Show paywall
      Alert.alert(
        'Itinerary Limit Reached',
        `You've used all ${usage.limit} free itineraries this month. Upgrade to Pro for unlimited itineraries.`,
        [
          { text: 'Maybe Later', style: 'cancel' },
          {
            text: 'Upgrade to Pro',
            onPress: () => navigation.navigate('Paywall', { source: 'limit_reached' }),
          },
        ]
      );
      return;
    }
  }

  // Proceed with itinerary generation
  setLoading(true);
  const itinerary = await itineraryAPI.generateItinerary(token, cityId);

  // Increment usage (backend handles Pro users automatically)
  await subscriptionAPI.incrementUsage(token);

  setLoading(false);
  navigation.navigate('Itinerary', { itinerary });
}
```

---

## Testing

### iOS - Sandbox Testing

1. **Create Sandbox Tester**:
   - App Store Connect → Users and Access → Sandbox Testers
   - Add email: `sandbox+test1@timbuktoo.ai`
   - Country: United States
   - Password: TestPassword123!

2. **Sign Out of Production Apple ID**:
   - Settings → [Your Name] → Media & Purchases → Sign Out

3. **Test Purchase Flow**:
   - Run app on device or simulator
   - Trigger paywall (e.g., Settings → Upgrade to Pro)
   - When prompted, sign in with sandbox tester account
   - Complete purchase (sandbox purchases are free)
   - Verify subscription activated in app

4. **Test Subscription Management**:
   - Settings → Manage Subscription (opens App Store)
   - Cancel subscription
   - Re-open app → verify subscription still active until expiration
   - Test auto-renewal (expires in 5 minutes in sandbox)

5. **Test Restore Purchases**:
   - Delete app
   - Reinstall app
   - Settings → Restore Purchases
   - Verify subscription restored

### Android - License Testing

1. **Add License Testers**:
   - Google Play Console → Setup → License Testing
   - Add email: `test@timbuktoo.ai`
   - License Response: RESPOND_NORMALLY

2. **Test Purchase Flow**:
   - Install app on device (must use email in license testers)
   - Trigger paywall
   - Complete purchase (test purchases are free and expire in 5 minutes)
   - Verify subscription activated

3. **Test Cancellation**:
   - Google Play → Subscriptions → Timbuktoo Pro → Cancel
   - Re-open app → verify still active until expiration

---

## App Store Compliance

### Required Legal Language

**Displayed on Paywall Screen** (see PaywallScreen.tsx above):

**iOS**:
```
Payment will be charged to your Apple ID account at confirmation of purchase.
Subscription automatically renews unless canceled at least 24 hours before the
end of the current period. Your account will be charged for renewal within 24
hours prior to the end of the current period. You can manage and cancel
subscriptions in your App Store account settings.
```

**Android**:
```
Payment will be charged to your Google account at confirmation of purchase.
Subscription automatically renews unless canceled at least 24 hours before the
end of the current period. You can manage and cancel subscriptions in your
Google Play account settings.
```

### Restore Purchases Button

**REQUIRED by Apple**: Must have a "Restore Purchases" button visible in Settings or Paywall.

**Implementation** (see SettingsScreen.tsx above):
```typescript
async function handleRestorePurchases() {
  setRestoring(true);
  const success = await restorePurchases();
  setRestoring(false);

  if (success) {
    Alert.alert('Subscription Restored', 'Your Pro subscription has been restored.');
  } else {
    Alert.alert('No Subscription Found', 'No active subscription to restore.');
  }
}
```

### App Review Notes

**Add to App_Review_Notes.txt**:
```
IN-APP PURCHASES:

This app offers two auto-renewable subscriptions:
1. Pro Monthly ($9.99/month) - Unlimited AI-generated itineraries
2. Pro Annual ($79.99/year) - Save 33%, unlimited itineraries

Free tier allows 3 itineraries per month.

Testing:
- Demo account (reviewer@timbuktoo.ai) is on FREE tier to demonstrate paywall
- Generate 3 itineraries to trigger paywall
- Use Sandbox Tester to complete purchase

Subscription Management:
- Settings → Manage Subscription (opens App Store)
- Settings → Restore Purchases (restores subscriptions on new device)

Legal Compliance:
- Auto-renewal disclosure displayed on paywall
- Terms of Service and Privacy Policy links on paywall
- "Restore Purchases" button in Settings
```

---

## Deployment Checklist

### Before Submitting to App Store

- [ ] RevenueCat API keys configured for production
- [ ] Subscription products created in App Store Connect (iOS)
- [ ] Subscription products created in Google Play Console (Android)
- [ ] RevenueCat webhook configured and tested
- [ ] Sandbox testing completed (iOS)
- [ ] License testing completed (Android)
- [ ] Paywall screen displays correct prices
- [ ] Legal language added to paywall
- [ ] "Restore Purchases" button added to Settings
- [ ] Backend subscription endpoints deployed
- [ ] Database schema created (subscriptions, itinerary_usage)
- [ ] App Review Notes updated with IAP testing instructions

---

## Common Issues

### Issue 1: "No Products Found"
**Cause**: Subscription products not synced from App Store Connect
**Fix**:
1. Wait 24 hours after creating products in App Store Connect
2. Clear app cache and rebuild
3. Verify Bundle ID matches App Store Connect

### Issue 2: "Purchase Failed - Already Owned"
**Cause**: Sandbox tester already owns subscription
**Fix**:
1. Delete sandbox tester from App Store Connect
2. Create new sandbox tester
3. Try purchase again

### Issue 3: "Receipt Validation Failed"
**Cause**: RevenueCat webhook not receiving events
**Fix**:
1. Check RevenueCat dashboard → Webhooks → Events
2. Verify webhook URL is publicly accessible
3. Check webhook signature verification

---

**Last Updated**: 2024-07-16
**Next Review**: Before App Store submission
