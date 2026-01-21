/**
 * Firebase Analytics Service
 * Tracks user events, screen views, and conversions
 */

import analytics from '@react-native-firebase/analytics';

// Event names (keep consistent for reporting)
export enum AnalyticsEvent {
  // Onboarding
  ONBOARDING_STARTED = 'onboarding_started',
  ONBOARDING_COMPLETED = 'onboarding_completed',
  AI_DISCLOSURE_ACCEPTED = 'ai_disclosure_accepted',
  DATA_USE_ACCEPTED = 'data_use_accepted',

  // Auth
  SIGNUP_STARTED = 'signup_started',
  SIGNUP_COMPLETED = 'signup_completed',
  LOGIN_STARTED = 'login_started',
  LOGIN_COMPLETED = 'login_completed',
  LOGOUT = 'logout',

  // Preferences
  PREFERENCES_SAVED = 'preferences_saved',
  PREFERENCES_UPDATED = 'preferences_updated',

  // Cities
  CITY_RECOMMENDATIONS_VIEWED = 'city_recommendations_viewed',
  CITY_SELECTED = 'city_selected',

  // Itineraries
  ITINERARY_GENERATION_STARTED = 'itinerary_generation_started',
  ITINERARY_GENERATION_COMPLETED = 'itinerary_generation_completed',
  ITINERARY_GENERATION_FAILED = 'itinerary_generation_failed',
  ITINERARY_VIEWED = 'itinerary_viewed',
  ITINERARY_RATED_HELPFUL = 'itinerary_rated_helpful',
  ITINERARY_RATED_NOT_HELPFUL = 'itinerary_rated_not_helpful',

  // Feedback
  FEEDBACK_SUBMITTED = 'feedback_submitted',

  // Subscriptions
  PAYWALL_VIEWED = 'paywall_viewed',
  SUBSCRIPTION_STARTED = 'subscription_started',
  SUBSCRIPTION_COMPLETED = 'subscription_completed',
  SUBSCRIPTION_CANCELLED = 'subscription_cancelled',
  SUBSCRIPTION_RESTORED = 'subscription_restored',

  // Settings
  SETTINGS_OPENED = 'settings_opened',
  ACCOUNT_DELETED = 'account_deleted',

  // Errors
  ERROR_OCCURRED = 'error_occurred',
}

/**
 * Initialize Firebase Analytics
 * Call this once when the app starts (in App.tsx)
 */
export async function initializeAnalytics(): Promise<void> {
  try {
    // Enable analytics collection
    await analytics().setAnalyticsCollectionEnabled(true);

    console.log('✅ Firebase Analytics initialized');
  } catch (error) {
    console.error('❌ Firebase Analytics initialization failed:', error);
  }
}

/**
 * Log a custom event
 */
export async function logEvent(
  eventName: AnalyticsEvent,
  params?: Record<string, any>
): Promise<void> {
  try {
    await analytics().logEvent(eventName, params);
    console.log(`📊 Event logged: ${eventName}`, params);
  } catch (error) {
    console.error(`❌ Failed to log event: ${eventName}`, error);
  }
}

/**
 * Log screen view
 */
export async function logScreenView(
  screenName: string,
  screenClass?: string
): Promise<void> {
  try {
    await analytics().logScreenView({
      screen_name: screenName,
      screen_class: screenClass || screenName,
    });
    console.log(`📱 Screen viewed: ${screenName}`);
  } catch (error) {
    console.error(`❌ Failed to log screen view: ${screenName}`, error);
  }
}

/**
 * Set user ID (after login/signup)
 */
export async function setUserId(userId: string): Promise<void> {
  try {
    await analytics().setUserId(userId);
    console.log(`👤 User ID set: ${userId}`);
  } catch (error) {
    console.error('❌ Failed to set user ID:', error);
  }
}

/**
 * Set user properties
 */
export async function setUserProperty(name: string, value: string): Promise<void> {
  try {
    await analytics().setUserProperty(name, value);
    console.log(`🏷️ User property set: ${name} = ${value}`);
  } catch (error) {
    console.error(`❌ Failed to set user property: ${name}`, error);
  }
}

/**
 * Clear user ID (on logout)
 */
export async function clearUserId(): Promise<void> {
  try {
    await analytics().setUserId(null);
    console.log('🗑️ User ID cleared');
  } catch (error) {
    console.error('❌ Failed to clear user ID:', error);
  }
}

// ============================================================================
// Convenience functions for common events
// ============================================================================

/**
 * Track signup flow
 */
export async function trackSignup(method: 'email' | 'social'): Promise<void> {
  await logEvent(AnalyticsEvent.SIGNUP_COMPLETED, {
    method,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track login flow
 */
export async function trackLogin(method: 'email' | 'social'): Promise<void> {
  await logEvent(AnalyticsEvent.LOGIN_COMPLETED, {
    method,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track preferences saved
 */
export async function trackPreferencesSaved(preferences: {
  interests: string[];
  foodPreferences: string[];
  budgetLevel: string;
  pace: string;
  tripLength: number;
}): Promise<void> {
  await logEvent(AnalyticsEvent.PREFERENCES_SAVED, {
    interests_count: preferences.interests.length,
    food_preferences_count: preferences.foodPreferences.length,
    budget_level: preferences.budgetLevel,
    pace: preferences.pace,
    trip_length: preferences.tripLength,
  });
}

/**
 * Track city selection
 */
export async function trackCitySelected(city: {
  name: string;
  country: string;
  matchScore?: number;
}): Promise<void> {
  await logEvent(AnalyticsEvent.CITY_SELECTED, {
    city_name: city.name,
    country: city.country,
    match_score: city.matchScore,
  });
}

/**
 * Track itinerary generation (start)
 */
export async function trackItineraryGenerationStarted(
  city: string,
  tripLength: number
): Promise<void> {
  await logEvent(AnalyticsEvent.ITINERARY_GENERATION_STARTED, {
    city,
    trip_length: tripLength,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track itinerary generation (complete)
 */
export async function trackItineraryGenerationCompleted(
  city: string,
  tripLength: number,
  generationTime: number
): Promise<void> {
  await logEvent(AnalyticsEvent.ITINERARY_GENERATION_COMPLETED, {
    city,
    trip_length: tripLength,
    generation_time_seconds: generationTime,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track itinerary generation failure
 */
export async function trackItineraryGenerationFailed(
  city: string,
  errorType: string
): Promise<void> {
  await logEvent(AnalyticsEvent.ITINERARY_GENERATION_FAILED, {
    city,
    error_type: errorType,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track itinerary rating
 */
export async function trackItineraryRating(
  itineraryId: string,
  helpful: boolean
): Promise<void> {
  await logEvent(
    helpful ? AnalyticsEvent.ITINERARY_RATED_HELPFUL : AnalyticsEvent.ITINERARY_RATED_NOT_HELPFUL,
    {
      itinerary_id: itineraryId,
      timestamp: new Date().toISOString(),
    }
  );
}

/**
 * Track feedback submission
 */
export async function trackFeedbackSubmitted(
  feedbackType: string,
  hasComments: boolean
): Promise<void> {
  await logEvent(AnalyticsEvent.FEEDBACK_SUBMITTED, {
    feedback_type: feedbackType,
    has_comments: hasComments,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track paywall view
 */
export async function trackPaywallViewed(source: string): Promise<void> {
  await logEvent(AnalyticsEvent.PAYWALL_VIEWED, {
    source, // e.g., 'rate_limit', 'settings', 'itinerary'
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track subscription purchase
 */
export async function trackSubscriptionPurchased(
  plan: 'monthly' | 'annual',
  price: number,
  currency: string
): Promise<void> {
  await logEvent(AnalyticsEvent.SUBSCRIPTION_COMPLETED, {
    plan,
    price,
    currency,
    timestamp: new Date().toISOString(),
  });

  // Also log Firebase's built-in purchase event
  await analytics().logPurchase({
    value: price,
    currency,
    items: [{ item_id: `pro_${plan}`, item_name: `Pro ${plan}` }],
  });
}

/**
 * Track error
 */
export async function trackError(
  errorType: string,
  errorMessage: string,
  context?: Record<string, any>
): Promise<void> {
  await logEvent(AnalyticsEvent.ERROR_OCCURRED, {
    error_type: errorType,
    error_message: errorMessage,
    ...context,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Track account deletion
 */
export async function trackAccountDeleted(
  reason?: string
): Promise<void> {
  await logEvent(AnalyticsEvent.ACCOUNT_DELETED, {
    reason: reason || 'not_specified',
    timestamp: new Date().toISOString(),
  });
}
