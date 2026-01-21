/**
 * RevenueCat Subscription Service
 * Handles Pro subscription purchases, status checks, and restoration
 */

import Purchases, {
  PurchasesPackage,
  PurchasesOffering,
  CustomerInfo,
  PurchasesError,
} from 'react-native-purchases';
import { Platform } from 'react-native';

// RevenueCat API Keys (add to .env)
const REVENUECAT_API_KEY_IOS = 'appl_YOUR_REVENUECAT_API_KEY';
const REVENUECAT_API_KEY_ANDROID = 'goog_YOUR_REVENUECAT_API_KEY';

// Entitlement identifier (configured in RevenueCat dashboard)
const PRO_ENTITLEMENT_ID = 'pro';

// Product IDs (must match App Store Connect / Google Play Console)
export const PRODUCT_IDS = {
  MONTHLY: Platform.OS === 'ios' ? 'ai.timbuktoo.mobile.pro.monthly' : 'pro_monthly',
  ANNUAL: Platform.OS === 'ios' ? 'ai.timbuktoo.mobile.pro.annual' : 'pro_annual',
};

/**
 * Initialize RevenueCat SDK
 * Call this once when the app starts (in App.tsx)
 */
export async function initializeRevenueCat(): Promise<void> {
  try {
    const apiKey = Platform.OS === 'ios' ? REVENUECAT_API_KEY_IOS : REVENUECAT_API_KEY_ANDROID;

    await Purchases.configure({ apiKey });

    // Enable debug logs in development
    if (__DEV__) {
      await Purchases.setLogLevel(Purchases.LOG_LEVEL.DEBUG);
    }

    console.log('✅ RevenueCat initialized');
  } catch (error) {
    console.error('❌ RevenueCat initialization failed:', error);
    throw error;
  }
}

/**
 * Check if user is a Pro subscriber
 */
export async function isProSubscriber(): Promise<boolean> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    const isPro = customerInfo.entitlements.active[PRO_ENTITLEMENT_ID] !== undefined;

    console.log(`🔍 Pro status: ${isPro}`);
    return isPro;
  } catch (error) {
    console.error('❌ Failed to check subscription status:', error);
    return false; // Default to false on error
  }
}

/**
 * Get available subscription offerings
 */
export async function getSubscriptionOfferings(): Promise<{
  monthly: PurchasesPackage | null;
  annual: PurchasesPackage | null;
}> {
  try {
    const offerings = await Purchases.getOfferings();

    if (!offerings.current) {
      console.warn('⚠️ No current offering available');
      return { monthly: null, annual: null };
    }

    const monthlyPackage = offerings.current.availablePackages.find(
      (pkg) => pkg.product.identifier === PRODUCT_IDS.MONTHLY
    );

    const annualPackage = offerings.current.availablePackages.find(
      (pkg) => pkg.product.identifier === PRODUCT_IDS.ANNUAL
    );

    return {
      monthly: monthlyPackage || null,
      annual: annualPackage || null,
    };
  } catch (error) {
    console.error('❌ Failed to fetch offerings:', error);
    return { monthly: null, annual: null };
  }
}

/**
 * Purchase a subscription package
 */
export async function purchaseSubscription(
  packageToPurchase: PurchasesPackage
): Promise<{
  success: boolean;
  isPro: boolean;
  error?: string;
}> {
  try {
    console.log(`🛒 Purchasing: ${packageToPurchase.product.identifier}`);

    const { customerInfo } = await Purchases.purchasePackage(packageToPurchase);
    const isPro = customerInfo.entitlements.active[PRO_ENTITLEMENT_ID] !== undefined;

    console.log(`✅ Purchase successful, Pro status: ${isPro}`);

    return {
      success: true,
      isPro,
    };
  } catch (error: any) {
    // Handle purchase cancellation (not an error)
    if (error.userCancelled) {
      console.log('ℹ️ User cancelled purchase');
      return {
        success: false,
        isPro: false,
        error: 'Purchase cancelled',
      };
    }

    // Handle other errors
    console.error('❌ Purchase failed:', error);

    let errorMessage = 'Purchase failed. Please try again.';

    if (error.code === 'PURCHASE_NOT_ALLOWED') {
      errorMessage = 'Purchases are not allowed on this device.';
    } else if (error.code === 'PRODUCT_ALREADY_PURCHASED') {
      errorMessage = 'You already have an active subscription.';
    } else if (error.code === 'NETWORK_ERROR') {
      errorMessage = 'Network error. Please check your connection.';
    }

    return {
      success: false,
      isPro: false,
      error: errorMessage,
    };
  }
}

/**
 * Restore previous purchases
 * Call this when user taps "Restore Purchases" button
 */
export async function restorePurchases(): Promise<{
  success: boolean;
  isPro: boolean;
  error?: string;
}> {
  try {
    console.log('🔄 Restoring purchases...');

    const customerInfo = await Purchases.restorePurchases();
    const isPro = customerInfo.entitlements.active[PRO_ENTITLEMENT_ID] !== undefined;

    console.log(`✅ Restore complete, Pro status: ${isPro}`);

    return {
      success: true,
      isPro,
    };
  } catch (error: any) {
    console.error('❌ Restore failed:', error);

    return {
      success: false,
      isPro: false,
      error: 'Failed to restore purchases. Please try again.',
    };
  }
}

/**
 * Get customer info (for displaying subscription details)
 */
export async function getCustomerInfo(): Promise<CustomerInfo | null> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    return customerInfo;
  } catch (error) {
    console.error('❌ Failed to get customer info:', error);
    return null;
  }
}

/**
 * Get subscription expiration date (if user is Pro)
 */
export async function getSubscriptionExpirationDate(): Promise<Date | null> {
  try {
    const customerInfo = await Purchases.getCustomerInfo();
    const proEntitlement = customerInfo.entitlements.active[PRO_ENTITLEMENT_ID];

    if (!proEntitlement) {
      return null; // Not a Pro subscriber
    }

    return proEntitlement.expirationDate ? new Date(proEntitlement.expirationDate) : null;
  } catch (error) {
    console.error('❌ Failed to get expiration date:', error);
    return null;
  }
}

/**
 * Format price for display
 */
export function formatPrice(packageItem: PurchasesPackage): string {
  const { product } = packageItem;
  return product.priceString; // Already formatted by RevenueCat (e.g., "$9.99")
}

/**
 * Calculate savings for annual plan
 */
export function calculateAnnualSavings(
  monthlyPackage: PurchasesPackage | null,
  annualPackage: PurchasesPackage | null
): { savings: number; savingsText: string } | null {
  if (!monthlyPackage || !annualPackage) {
    return null;
  }

  const monthlyPrice = monthlyPackage.product.price;
  const annualPrice = annualPackage.product.price;

  const annualMonthlyEquivalent = monthlyPrice * 12;
  const savings = annualMonthlyEquivalent - annualPrice;
  const savingsPercentage = Math.round((savings / annualMonthlyEquivalent) * 100);

  return {
    savings,
    savingsText: `Save ${savingsPercentage}% (${monthlyPackage.product.currencyCode} ${savings.toFixed(2)}/year)`,
  };
}

/**
 * Set user ID for attribution (call after login/signup)
 */
export async function setUserIdForAttribution(userId: string): Promise<void> {
  try {
    await Purchases.logIn(userId);
    console.log(`✅ User ID set for RevenueCat: ${userId}`);
  } catch (error) {
    console.error('❌ Failed to set user ID:', error);
  }
}

/**
 * Log out user from RevenueCat (call on logout)
 */
export async function logoutRevenueCat(): Promise<void> {
  try {
    await Purchases.logOut();
    console.log('✅ Logged out from RevenueCat');
  } catch (error) {
    console.error('❌ Failed to logout from RevenueCat:', error);
  }
}
