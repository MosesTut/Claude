/**
 * Offline Support & Caching Service
 * Cache itineraries and preferences locally for offline access
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { Itinerary, Preferences, CityRecommendation } from '../types';

// Cache keys
const CACHE_KEYS = {
  PREFERENCES: '@timbuktoo/preferences',
  ITINERARIES: '@timbuktoo/itineraries',
  CITY_RECOMMENDATIONS: '@timbuktoo/city_recommendations',
  LAST_SYNC: '@timbuktoo/last_sync',
  OFFLINE_QUEUE: '@timbuktoo/offline_queue',
};

// Cache expiration (in milliseconds)
const CACHE_EXPIRATION = {
  PREFERENCES: 7 * 24 * 60 * 60 * 1000, // 7 days
  ITINERARIES: 30 * 24 * 60 * 60 * 1000, // 30 days
  CITY_RECOMMENDATIONS: 24 * 60 * 60 * 1000, // 24 hours
};

interface CachedData<T> {
  data: T;
  timestamp: number;
  expiresAt: number;
}

// ============================================================================
// Generic Cache Functions
// ============================================================================

/**
 * Save data to cache with expiration
 */
async function saveToCache<T>(
  key: string,
  data: T,
  expirationMs: number
): Promise<void> {
  try {
    const cachedData: CachedData<T> = {
      data,
      timestamp: Date.now(),
      expiresAt: Date.now() + expirationMs,
    };

    await AsyncStorage.setItem(key, JSON.stringify(cachedData));
    console.log(`✅ Saved to cache: ${key}`);
  } catch (error) {
    console.error(`❌ Failed to save to cache: ${key}`, error);
  }
}

/**
 * Load data from cache (returns null if expired or not found)
 */
async function loadFromCache<T>(key: string): Promise<T | null> {
  try {
    const cachedString = await AsyncStorage.getItem(key);

    if (!cachedString) {
      return null;
    }

    const cachedData: CachedData<T> = JSON.parse(cachedString);

    // Check if expired
    if (Date.now() > cachedData.expiresAt) {
      console.log(`⏰ Cache expired: ${key}`);
      await AsyncStorage.removeItem(key);
      return null;
    }

    console.log(`✅ Loaded from cache: ${key}`);
    return cachedData.data;
  } catch (error) {
    console.error(`❌ Failed to load from cache: ${key}`, error);
    return null;
  }
}

/**
 * Remove data from cache
 */
async function removeFromCache(key: string): Promise<void> {
  try {
    await AsyncStorage.removeItem(key);
    console.log(`🗑️ Removed from cache: ${key}`);
  } catch (error) {
    console.error(`❌ Failed to remove from cache: ${key}`, error);
  }
}

/**
 * Clear all cache
 */
export async function clearAllCache(): Promise<void> {
  try {
    await AsyncStorage.clear();
    console.log('🗑️ All cache cleared');
  } catch (error) {
    console.error('❌ Failed to clear cache:', error);
  }
}

// ============================================================================
// Preferences Caching
// ============================================================================

/**
 * Cache user preferences
 */
export async function cachePreferences(preferences: Preferences): Promise<void> {
  await saveToCache(CACHE_KEYS.PREFERENCES, preferences, CACHE_EXPIRATION.PREFERENCES);
}

/**
 * Load cached preferences
 */
export async function loadCachedPreferences(): Promise<Preferences | null> {
  return await loadFromCache<Preferences>(CACHE_KEYS.PREFERENCES);
}

/**
 * Clear cached preferences
 */
export async function clearCachedPreferences(): Promise<void> {
  await removeFromCache(CACHE_KEYS.PREFERENCES);
}

// ============================================================================
// Itineraries Caching
// ============================================================================

/**
 * Cache multiple itineraries
 */
export async function cacheItineraries(itineraries: Itinerary[]): Promise<void> {
  await saveToCache(CACHE_KEYS.ITINERARIES, itineraries, CACHE_EXPIRATION.ITINERARIES);
}

/**
 * Load cached itineraries
 */
export async function loadCachedItineraries(): Promise<Itinerary[] | null> {
  return await loadFromCache<Itinerary[]>(CACHE_KEYS.ITINERARIES);
}

/**
 * Add single itinerary to cache
 */
export async function addItineraryToCache(itinerary: Itinerary): Promise<void> {
  try {
    const existing = await loadCachedItineraries();
    const itineraries = existing || [];

    // Check if itinerary already exists (update it)
    const index = itineraries.findIndex((i) => i.id === itinerary.id);
    if (index !== -1) {
      itineraries[index] = itinerary;
    } else {
      itineraries.unshift(itinerary); // Add to beginning
    }

    // Keep only last 10 itineraries
    const limited = itineraries.slice(0, 10);
    await cacheItineraries(limited);
  } catch (error) {
    console.error('❌ Failed to add itinerary to cache:', error);
  }
}

/**
 * Get single itinerary from cache by ID
 */
export async function getCachedItineraryById(id: string): Promise<Itinerary | null> {
  try {
    const itineraries = await loadCachedItineraries();
    if (!itineraries) return null;

    return itineraries.find((i) => i.id === id) || null;
  } catch (error) {
    console.error('❌ Failed to get cached itinerary:', error);
    return null;
  }
}

/**
 * Clear cached itineraries
 */
export async function clearCachedItineraries(): Promise<void> {
  await removeFromCache(CACHE_KEYS.ITINERARIES);
}

// ============================================================================
// City Recommendations Caching
// ============================================================================

/**
 * Cache city recommendations
 */
export async function cacheCityRecommendations(
  cities: CityRecommendation[]
): Promise<void> {
  await saveToCache(
    CACHE_KEYS.CITY_RECOMMENDATIONS,
    cities,
    CACHE_EXPIRATION.CITY_RECOMMENDATIONS
  );
}

/**
 * Load cached city recommendations
 */
export async function loadCachedCityRecommendations(): Promise<CityRecommendation[] | null> {
  return await loadFromCache<CityRecommendation[]>(CACHE_KEYS.CITY_RECOMMENDATIONS);
}

/**
 * Clear cached city recommendations
 */
export async function clearCachedCityRecommendations(): Promise<void> {
  await removeFromCache(CACHE_KEYS.CITY_RECOMMENDATIONS);
}

// ============================================================================
// Offline Queue (for actions to sync when online)
// ============================================================================

export interface OfflineAction {
  id: string;
  type: 'rate_itinerary' | 'submit_feedback' | 'update_preferences';
  payload: any;
  timestamp: number;
}

/**
 * Add action to offline queue
 */
export async function addToOfflineQueue(
  type: OfflineAction['type'],
  payload: any
): Promise<void> {
  try {
    const queue = await loadOfflineQueue();

    const action: OfflineAction = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      payload,
      timestamp: Date.now(),
    };

    queue.push(action);
    await AsyncStorage.setItem(CACHE_KEYS.OFFLINE_QUEUE, JSON.stringify(queue));
    console.log(`✅ Added to offline queue: ${type}`);
  } catch (error) {
    console.error('❌ Failed to add to offline queue:', error);
  }
}

/**
 * Load offline queue
 */
export async function loadOfflineQueue(): Promise<OfflineAction[]> {
  try {
    const queueString = await AsyncStorage.getItem(CACHE_KEYS.OFFLINE_QUEUE);
    if (!queueString) return [];

    return JSON.parse(queueString);
  } catch (error) {
    console.error('❌ Failed to load offline queue:', error);
    return [];
  }
}

/**
 * Process offline queue (when back online)
 */
export async function processOfflineQueue(
  apiClient: any
): Promise<{ success: number; failed: number }> {
  try {
    const queue = await loadOfflineQueue();
    if (queue.length === 0) {
      console.log('ℹ️ Offline queue is empty');
      return { success: 0, failed: 0 };
    }

    console.log(`📤 Processing ${queue.length} offline actions...`);

    let success = 0;
    let failed = 0;
    const remaining: OfflineAction[] = [];

    for (const action of queue) {
      try {
        // Process based on type
        switch (action.type) {
          case 'rate_itinerary':
            await apiClient.patch(
              `/itinerary/${action.payload.itineraryId}/rating`,
              { helpful: action.payload.helpful }
            );
            break;

          case 'submit_feedback':
            await apiClient.post('/feedback', action.payload);
            break;

          case 'update_preferences':
            await apiClient.post('/preferences', action.payload);
            break;

          default:
            console.warn(`⚠️ Unknown action type: ${action.type}`);
        }

        success++;
        console.log(`✅ Processed: ${action.type}`);
      } catch (error) {
        console.error(`❌ Failed to process: ${action.type}`, error);
        remaining.push(action); // Keep failed actions for retry
        failed++;
      }
    }

    // Save remaining failed actions
    await AsyncStorage.setItem(CACHE_KEYS.OFFLINE_QUEUE, JSON.stringify(remaining));
    console.log(`📊 Queue processed: ${success} success, ${failed} failed`);

    return { success, failed };
  } catch (error) {
    console.error('❌ Failed to process offline queue:', error);
    return { success: 0, failed: 0 };
  }
}

/**
 * Clear offline queue
 */
export async function clearOfflineQueue(): Promise<void> {
  await removeFromCache(CACHE_KEYS.OFFLINE_QUEUE);
}

// ============================================================================
// Last Sync Tracking
// ============================================================================

/**
 * Update last sync timestamp
 */
export async function updateLastSync(): Promise<void> {
  try {
    await AsyncStorage.setItem(CACHE_KEYS.LAST_SYNC, Date.now().toString());
    console.log('✅ Last sync updated');
  } catch (error) {
    console.error('❌ Failed to update last sync:', error);
  }
}

/**
 * Get last sync timestamp
 */
export async function getLastSync(): Promise<Date | null> {
  try {
    const timestamp = await AsyncStorage.getItem(CACHE_KEYS.LAST_SYNC);
    if (!timestamp) return null;

    return new Date(parseInt(timestamp));
  } catch (error) {
    console.error('❌ Failed to get last sync:', error);
    return null;
  }
}

/**
 * Check if data needs sync (older than X hours)
 */
export async function needsSync(hoursThreshold: number = 24): Promise<boolean> {
  const lastSync = await getLastSync();
  if (!lastSync) return true;

  const hoursSinceSync = (Date.now() - lastSync.getTime()) / (1000 * 60 * 60);
  return hoursSinceSync >= hoursThreshold;
}
