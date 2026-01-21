/**
 * Push Notifications Service (Expo Notifications)
 * Handles push notification registration, permissions, and handling
 */

import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import { Platform } from 'react-native';
import Constants from 'expo-constants';

// Configure how notifications are displayed when app is in foreground
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

/**
 * Register for push notifications and get Expo Push Token
 * Call this after user logs in
 */
export async function registerForPushNotifications(): Promise<string | null> {
  try {
    // Check if running on physical device
    if (!Device.isDevice) {
      console.warn('⚠️ Push notifications only work on physical devices');
      return null;
    }

    // Check existing permissions
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;

    // Request permission if not granted
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }

    if (finalStatus !== 'granted') {
      console.warn('⚠️ Push notification permission denied');
      return null;
    }

    // Get Expo Push Token
    const projectId = Constants.expoConfig?.extra?.eas?.projectId;
    if (!projectId) {
      console.error('❌ Expo project ID not found in app.json');
      return null;
    }

    const token = (await Notifications.getExpoPushTokenAsync({ projectId })).data;
    console.log('✅ Expo Push Token:', token);

    // Configure notification channel for Android
    if (Platform.OS === 'android') {
      await Notifications.setNotificationChannelAsync('default', {
        name: 'default',
        importance: Notifications.AndroidImportance.MAX,
        vibrationPattern: [0, 250, 250, 250],
        lightColor: '#8B5CF6',
      });
    }

    return token;
  } catch (error) {
    console.error('❌ Failed to register for push notifications:', error);
    return null;
  }
}

/**
 * Send push token to backend
 * Call this after getting the token
 */
export async function sendPushTokenToBackend(
  token: string,
  apiClient: any
): Promise<void> {
  try {
    await apiClient.post('/user/push-token', {
      push_token: token,
      platform: Platform.OS,
    });
    console.log('✅ Push token sent to backend');
  } catch (error) {
    console.error('❌ Failed to send push token to backend:', error);
  }
}

/**
 * Schedule a local notification
 * Used for reminders, etc.
 */
export async function scheduleLocalNotification(
  title: string,
  body: string,
  trigger: Notifications.NotificationTriggerInput
): Promise<string> {
  try {
    const identifier = await Notifications.scheduleNotificationAsync({
      content: {
        title,
        body,
        sound: true,
        priority: Notifications.AndroidNotificationPriority.HIGH,
      },
      trigger,
    });

    console.log(`✅ Local notification scheduled: ${identifier}`);
    return identifier;
  } catch (error) {
    console.error('❌ Failed to schedule local notification:', error);
    throw error;
  }
}

/**
 * Cancel a scheduled notification
 */
export async function cancelScheduledNotification(identifier: string): Promise<void> {
  try {
    await Notifications.cancelScheduledNotificationAsync(identifier);
    console.log(`✅ Notification cancelled: ${identifier}`);
  } catch (error) {
    console.error('❌ Failed to cancel notification:', error);
  }
}

/**
 * Cancel all scheduled notifications
 */
export async function cancelAllNotifications(): Promise<void> {
  try {
    await Notifications.cancelAllScheduledNotificationsAsync();
    console.log('✅ All notifications cancelled');
  } catch (error) {
    console.error('❌ Failed to cancel all notifications:', error);
  }
}

/**
 * Get badge count
 */
export async function getBadgeCount(): Promise<number> {
  try {
    return await Notifications.getBadgeCountAsync();
  } catch (error) {
    console.error('❌ Failed to get badge count:', error);
    return 0;
  }
}

/**
 * Set badge count
 */
export async function setBadgeCount(count: number): Promise<void> {
  try {
    await Notifications.setBadgeCountAsync(count);
    console.log(`✅ Badge count set to: ${count}`);
  } catch (error) {
    console.error('❌ Failed to set badge count:', error);
  }
}

/**
 * Clear badge count
 */
export async function clearBadgeCount(): Promise<void> {
  await setBadgeCount(0);
}

/**
 * Add notification received listener (when app is in foreground)
 */
export function addNotificationReceivedListener(
  handler: (notification: Notifications.Notification) => void
): Notifications.Subscription {
  return Notifications.addNotificationReceivedListener(handler);
}

/**
 * Add notification response listener (when user taps notification)
 */
export function addNotificationResponseReceivedListener(
  handler: (response: Notifications.NotificationResponse) => void
): Notifications.Subscription {
  return Notifications.addNotificationResponseReceivedListener(handler);
}

/**
 * Remove notification listener
 */
export function removeNotificationSubscription(
  subscription: Notifications.Subscription
): void {
  subscription.remove();
}

// ============================================================================
// Predefined Notification Templates
// ============================================================================

/**
 * Schedule trip reminder notification
 * Remind user X days before their trip
 */
export async function scheduleTripReminder(
  cityName: string,
  tripDate: Date,
  daysBeforeTrip: number = 3
): Promise<string | null> {
  try {
    const reminderDate = new Date(tripDate);
    reminderDate.setDate(reminderDate.getDate() - daysBeforeTrip);

    // Only schedule if reminder date is in the future
    if (reminderDate <= new Date()) {
      console.warn('⚠️ Trip reminder date is in the past');
      return null;
    }

    const identifier = await scheduleLocalNotification(
      `Trip to ${cityName} is coming up!`,
      `Your trip is in ${daysBeforeTrip} days. Check your itinerary to prepare.`,
      {
        date: reminderDate,
      }
    );

    return identifier;
  } catch (error) {
    console.error('❌ Failed to schedule trip reminder:', error);
    return null;
  }
}

/**
 * Schedule feedback reminder
 * Remind user to rate their itinerary after trip
 */
export async function scheduleFeedbackReminder(
  cityName: string,
  tripEndDate: Date
): Promise<string | null> {
  try {
    const reminderDate = new Date(tripEndDate);
    reminderDate.setDate(reminderDate.getDate() + 1); // Day after trip ends

    const identifier = await scheduleLocalNotification(
      `How was ${cityName}?`,
      `We'd love to hear about your trip! Rate your itinerary to help us improve.`,
      {
        date: reminderDate,
      }
    );

    return identifier;
  } catch (error) {
    console.error('❌ Failed to schedule feedback reminder:', error);
    return null;
  }
}

/**
 * Schedule pro trial ending reminder
 * Remind user 1 day before trial ends
 */
export async function scheduleTrialEndingReminder(
  trialEndDate: Date
): Promise<string | null> {
  try {
    const reminderDate = new Date(trialEndDate);
    reminderDate.setDate(reminderDate.getDate() - 1); // 1 day before

    const identifier = await scheduleLocalNotification(
      'Your Pro trial ends tomorrow',
      'Continue unlimited itinerary generation by keeping your Pro subscription.',
      {
        date: reminderDate,
      }
    );

    return identifier;
  } catch (error) {
    console.error('❌ Failed to schedule trial reminder:', error);
    return null;
  }
}

/**
 * Notification preferences (stored locally)
 */
export interface NotificationPreferences {
  tripReminders: boolean;
  feedbackReminders: boolean;
  promotionalNotifications: boolean;
  trialReminders: boolean;
}

const DEFAULT_PREFERENCES: NotificationPreferences = {
  tripReminders: true,
  feedbackReminders: true,
  promotionalNotifications: false,
  trialReminders: true,
};

// In a real app, store these in AsyncStorage or SecureStore
let cachedPreferences: NotificationPreferences = DEFAULT_PREFERENCES;

export function getNotificationPreferences(): NotificationPreferences {
  return cachedPreferences;
}

export function setNotificationPreferences(
  preferences: Partial<NotificationPreferences>
): void {
  cachedPreferences = { ...cachedPreferences, ...preferences };
  console.log('✅ Notification preferences updated:', cachedPreferences);
  // TODO: Save to AsyncStorage
}
