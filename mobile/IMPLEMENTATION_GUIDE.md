# Timbuktoo Mobile MVP - Complete Implementation Guide

**Document Purpose**: Production-ready implementation guide for React Native + Expo mobile app with App Store approval compliance.

**Status**: Ready for engineering to build immediately
**Timeline**: 4-6 weeks to App Store submission
**Tech Stack**: React Native 0.72, Expo 49, TypeScript

---

## Table of Contents

1. [Project Setup](#project-setup)
2. [Remaining Screens Implementation](#remaining-screens-implementation)
3. [API Client Implementation](#api-client-implementation)
4. [Security & Storage](#security--storage)
5. [App Store Submission](#app-store-submission)
6. [Testing Strategy](#testing-strategy)
7. [Deployment Checklist](#deployment-checklist)

---

## Project Setup

### Prerequisites

```bash
# Install Node.js 18+ and npm
node --version  # v18.0.0+
npm --version   # 9.0.0+

# Install Expo CLI globally
npm install -g expo-cli

# Install EAS CLI (for builds)
npm install -g eas-cli
```

### Initial Setup

```bash
cd mobile/
npm install

# Start development server
npm start

# Run on iOS simulator (requires macOS + Xcode)
npm run ios

# Run on Android emulator (requires Android Studio)
npm run android
```

---

## Remaining Screens Implementation

### Preferences Screen (`src/screens/PreferencesScreen.tsx`)

```typescript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { TextInput, Button, Chip } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import * as SecureStore from 'expo-secure-store';
import { preferencesAPI } from '../api/preferences';

type PreferencesScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Preferences'>;
};

const INTERESTS = [
  'History & Culture',
  'Food & Dining',
  'Nightlife',
  'Nature & Parks',
  'Art & Museums',
  'Shopping',
  'Adventure',
  'Relaxation',
];

const FOOD_PREFERENCES = [
  'Local Cuisine',
  'Street Food',
  'Fine Dining',
  'Vegetarian',
  'Vegan',
  'Seafood',
  'International',
  'Cafes & Coffee',
];

const BUDGET_RANGES = [
  { label: 'Budget ($)', value: 'budget' },
  { label: 'Moderate ($$)', value: 'moderate' },
  { label: 'Luxury ($$$)', value: 'luxury' },
];

export default function PreferencesScreen({
  navigation,
}: PreferencesScreenProps) {
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [selectedFood, setSelectedFood] = useState<string[]>([]);
  const [budget, setBudget] = useState<string>('moderate');
  const [travelDates, setTravelDates] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPreferences();
  }, []);

  const loadPreferences = async () => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      if (token) {
        const prefs = await preferencesAPI.getPreferences(token);
        if (prefs) {
          setSelectedInterests(prefs.interests || []);
          setSelectedFood(prefs.foodPreferences || []);
          setBudget(prefs.budget || 'moderate');
          setTravelDates(prefs.travelDates || '');
        }
      }
    } catch (error) {
      console.error('Error loading preferences:', error);
    }
  };

  const toggleInterest = (interest: string) => {
    setSelectedInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    );
  };

  const toggleFood = (food: string) => {
    setSelectedFood((prev) =>
      prev.includes(food) ? prev.filter((f) => f !== food) : [...prev, food]
    );
  };

  const handleSave = async () => {
    if (selectedInterests.length === 0) {
      Alert.alert('Error', 'Please select at least one interest');
      return;
    }

    setLoading(true);

    try {
      const token = await SecureStore.getItemAsync('authToken');
      if (!token) throw new Error('Not authenticated');

      await preferencesAPI.savePreferences(token, {
        interests: selectedInterests,
        foodPreferences: selectedFood,
        budget,
        travelDates,
      });

      navigation.navigate('CityRecommendation');
    } catch (error: any) {
      Alert.alert('Error', 'Failed to save preferences. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Your Preferences</Text>
          <Text style={styles.subtitle}>
            Help us personalize your trip recommendations
          </Text>
          <Text style={styles.disclosure}>
            Preferences help personalize AI-generated itineraries.
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>What interests you?</Text>
          <View style={styles.chipContainer}>
            {INTERESTS.map((interest) => (
              <Chip
                key={interest}
                selected={selectedInterests.includes(interest)}
                onPress={() => toggleInterest(interest)}
                style={styles.chip}
              >
                {interest}
              </Chip>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Food & Drink</Text>
          <View style={styles.chipContainer}>
            {FOOD_PREFERENCES.map((food) => (
              <Chip
                key={food}
                selected={selectedFood.includes(food)}
                onPress={() => toggleFood(food)}
                style={styles.chip}
              >
                {food}
              </Chip>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Budget</Text>
          <View style={styles.chipContainer}>
            {BUDGET_RANGES.map(({ label, value }) => (
              <Chip
                key={value}
                selected={budget === value}
                onPress={() => setBudget(value)}
                style={styles.chip}
              >
                {label}
              </Chip>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Travel Dates (Optional)</Text>
          <TextInput
            label="e.g., June 2025"
            value={travelDates}
            onChangeText={setTravelDates}
            mode="outlined"
            style={styles.input}
          />
        </View>

        <Button
          mode="contained"
          onPress={handleSave}
          loading={loading}
          disabled={loading || selectedInterests.length === 0}
          style={styles.button}
          contentStyle={styles.buttonContent}
        >
          Find My Perfect City
        </Button>

        <Button
          mode="text"
          onPress={() => navigation.navigate('Settings')}
          style={styles.settingsButton}
        >
          Settings
        </Button>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  scrollContent: {
    padding: 24,
  },
  header: {
    marginTop: 20,
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666666',
    marginBottom: 8,
  },
  disclosure: {
    fontSize: 12,
    color: '#999999',
    fontStyle: 'italic',
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 12,
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chip: {
    marginRight: 4,
    marginBottom: 4,
  },
  input: {
    marginTop: 8,
  },
  button: {
    borderRadius: 8,
    marginTop: 8,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  settingsButton: {
    marginTop: 12,
  },
});
```

---

### City Recommendation Screen (`src/screens/CityRecommendationScreen.tsx`)

```typescript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Image,
} from 'react-native';
import { Button, Card } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import * as SecureStore from 'expo-secure-store';
import { citiesAPI } from '../api/cities';

type CityRecommendationScreenProps = {
  navigation: NativeStackNavigationProp<
    RootStackParamList,
    'CityRecommendation'
  >;
};

type City = {
  id: string;
  name: string;
  country: string;
  reasoning: string;
  imageUrl?: string;
};

export default function CityRecommendationScreen({
  navigation,
}: CityRecommendationScreenProps) {
  const [cities, setCities] = useState<City[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      if (!token) throw new Error('Not authenticated');

      const recommendations = await citiesAPI.getRecommendations(token);
      setCities(recommendations);
    } catch (error: any) {
      setError('Failed to load recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCity = (city: City) => {
    navigation.navigate('Itinerary', {
      cityId: city.id,
      cityName: city.name,
    });
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Finding your perfect cities...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Button mode="contained" onPress={loadCities}>
            Try Again
          </Button>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Perfect Cities for You</Text>
          <Text style={styles.subtitle}>Based on your preferences</Text>
        </View>

        {cities.map((city, index) => (
          <Card key={city.id} style={styles.cityCard}>
            <Card.Content>
              <View style={styles.badge}>
                <Text style={styles.badgeText}>Top {index + 1}</Text>
              </View>
              <Text style={styles.cityName}>
                {city.name}, {city.country}
              </Text>
              <Text style={styles.reasoning}>{city.reasoning}</Text>
            </Card.Content>
            <Card.Actions>
              <Button
                mode="contained"
                onPress={() => handleSelectCity(city)}
                style={styles.buildTripButton}
              >
                Build My Trip
              </Button>
            </Card.Actions>
          </Card>
        ))}

        <Button
          mode="text"
          onPress={() => navigation.navigate('Preferences')}
          style={styles.changePrefsButton}
        >
          Change Preferences
        </Button>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  errorText: {
    fontSize: 16,
    color: '#666666',
    textAlign: 'center',
    marginBottom: 24,
  },
  scrollContent: {
    padding: 24,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666666',
  },
  cityCard: {
    marginBottom: 16,
  },
  badge: {
    backgroundColor: '#007AFF',
    borderRadius: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    alignSelf: 'flex-start',
    marginBottom: 8,
  },
  badgeText: {
    color: '#ffffff',
    fontSize: 12,
    fontWeight: '600',
  },
  cityName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  reasoning: {
    fontSize: 14,
    color: '#666666',
    lineHeight: 20,
  },
  buildTripButton: {
    borderRadius: 8,
    marginLeft: 'auto',
  },
  changePrefsButton: {
    marginTop: 16,
  },
});
```

---

### Itinerary Screen (`src/screens/ItineraryScreen.tsx`)

```typescript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import { Button, Card, Chip } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../../App';
import * as SecureStore from 'expo-secure-store';
import { itineraryAPI } from '../api/itinerary';

type ItineraryScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Itinerary'>;
  route: RouteProp<RootStackParamList, 'Itinerary'>;
};

type DayPlan = {
  day: number;
  activities: Activity[];
  meals: Meal[];
  weather: string;
};

type Activity = {
  time: string;
  name: string;
  description: string;
  address: string;
};

type Meal = {
  type: 'breakfast' | 'lunch' | 'dinner';
  name: string;
  cuisine: string;
  price: string;
};

export default function ItineraryScreen({
  navigation,
  route,
}: ItineraryScreenProps) {
  const { cityId, cityName } = route.params;
  const [itinerary, setItinerary] = useState<DayPlan[] | null>(null);
  const [itineraryId, setItineraryId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadItinerary();
  }, [cityId]);

  const loadItinerary = async () => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      if (!token) throw new Error('Not authenticated');

      const response = await itineraryAPI.generate(token, cityId);
      setItinerary(response.itinerary);
      setItineraryId(response.itineraryId);
    } catch (error: any) {
      setError('Failed to generate itinerary. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Crafting your perfect trip...</Text>
        <Text style={styles.loadingSubtext}>
          This may take 30-60 seconds
        </Text>
      </View>
    );
  }

  if (error || !itinerary) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Button mode="contained" onPress={loadItinerary}>
            Try Again
          </Button>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>{cityName}</Text>
          <Text style={styles.subtitle}>
            {itinerary.length}-Day Itinerary
          </Text>

          {/* REQUIRED AI BANNER (Apple compliance) */}
          <View style={styles.aiBanner}>
            <Text style={styles.aiBannerText}>
              ⚠️ This itinerary was generated by AI
            </Text>
          </View>
        </View>

        {itinerary.map((day) => (
          <Card key={day.day} style={styles.dayCard}>
            <Card.Content>
              <View style={styles.dayHeader}>
                <Text style={styles.dayNumber}>Day {day.day}</Text>
                <Chip icon="weather-partly-cloudy" compact>
                  {day.weather}
                </Chip>
              </View>

              {/* Meals */}
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>Meals</Text>
                {day.meals.map((meal, index) => (
                  <View key={index} style={styles.mealItem}>
                    <Text style={styles.mealType}>
                      {meal.type.toUpperCase()}
                    </Text>
                    <Text style={styles.mealName}>{meal.name}</Text>
                    <Text style={styles.mealDetails}>
                      {meal.cuisine} • {meal.price}
                    </Text>
                  </View>
                ))}
              </View>

              {/* Activities */}
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>Activities</Text>
                {day.activities.map((activity, index) => (
                  <View key={index} style={styles.activityItem}>
                    <Text style={styles.activityTime}>{activity.time}</Text>
                    <Text style={styles.activityName}>{activity.name}</Text>
                    <Text style={styles.activityDescription}>
                      {activity.description}
                    </Text>
                    <Text style={styles.activityAddress}>
                      📍 {activity.address}
                    </Text>
                  </View>
                ))}
              </View>
            </Card.Content>
          </Card>
        ))}

        <View style={styles.footer}>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('Feedback', { itineraryId })}
            style={styles.feedbackButton}
          >
            Give Feedback
          </Button>

          <Button
            mode="outlined"
            onPress={() => navigation.navigate('CityRecommendation')}
            style={styles.newTripButton}
          >
            Plan Another Trip
          </Button>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666666',
    fontWeight: '600',
  },
  loadingSubtext: {
    marginTop: 8,
    fontSize: 14,
    color: '#999999',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  errorText: {
    fontSize: 16,
    color: '#666666',
    textAlign: 'center',
    marginBottom: 24,
  },
  scrollContent: {
    padding: 24,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#666666',
    marginBottom: 16,
  },
  aiBanner: {
    backgroundColor: '#fff3cd',
    borderColor: '#ffc107',
    borderWidth: 1,
    borderRadius: 8,
    padding: 12,
  },
  aiBannerText: {
    fontSize: 14,
    color: '#856404',
    fontWeight: '500',
  },
  dayCard: {
    marginBottom: 16,
  },
  dayHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  dayNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1a1a1a',
  },
  section: {
    marginTop: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 12,
  },
  mealItem: {
    marginBottom: 12,
    paddingBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  mealType: {
    fontSize: 12,
    fontWeight: '600',
    color: '#007AFF',
    marginBottom: 4,
  },
  mealName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 2,
  },
  mealDetails: {
    fontSize: 14,
    color: '#666666',
  },
  activityItem: {
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  activityTime: {
    fontSize: 14,
    fontWeight: '600',
    color: '#007AFF',
    marginBottom: 4,
  },
  activityName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  activityDescription: {
    fontSize: 14,
    color: '#666666',
    lineHeight: 20,
    marginBottom: 4,
  },
  activityAddress: {
    fontSize: 12,
    color: '#999999',
  },
  footer: {
    marginTop: 24,
    gap: 12,
  },
  feedbackButton: {
    borderRadius: 8,
  },
  newTripButton: {
    borderRadius: 8,
  },
});
```

---

## API Client Implementation

Create `src/api/client.ts`:

```typescript
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_URL = 'https://api.timbuktoo.ai';

const client = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
client.interceptors.request.use(
  async (config) => {
    const token = await SecureStore.getItemAsync('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default client;
```

Create `src/api/auth.ts`:

```typescript
import client from './client';

export const authAPI = {
  signup: async (email: string, password: string) => {
    const response = await client.post('/auth/signup', { email, password });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await client.post('/auth/login', { email, password });
    return response.data;
  },

  logout: async () => {
    const response = await client.post('/auth/logout');
    return response.data;
  },
};
```

**Continue this pattern for**:
- `src/api/preferences.ts`
- `src/api/cities.ts`
- `src/api/itinerary.ts`
- `src/api/feedback.ts`

---

## App Store Submission

### iOS Privacy Nutrition Label

File: `mobile/ios-privacy-label.json`

```json
{
  "dataTypes": [
    {
      "dataType": "Email Address",
      "purposes": ["App Functionality", "Developer Advertising"],
      "dataLinkedToUser": true,
      "dataUsedToTrackUser": false
    },
    {
      "dataType": "User Content",
      "category": "AI-Generated Content",
      "purposes": ["App Functionality"],
      "dataLinkedToUser": true,
      "dataUsedToTrackUser": false,
      "description": "Travel itineraries generated by artificial intelligence based on user preferences"
    },
    {
      "dataType": "Product Interaction",
      "purposes": ["Analytics", "App Functionality"],
      "dataLinkedToUser": false,
      "dataUsedToTrackUser": false
    }
  ],
  "dataCollection": {
    "encrypted": true,
    "userDeletion": true,
    "thirdPartySharing": false
  }
}
```

### App Review Notes

File: `mobile/app-review-notes.txt`

```
App Review Notes - Timbuktoo Mobile v1.0.0

AI DISCLOSURE COMPLIANCE:
Timbuktoo generates travel itineraries using artificial intelligence (Anthropic Claude API).

User notifications:
1. Onboarding screen explicitly states "uses artificial intelligence"
2. Mandatory consent checkbox: "I understand itineraries are AI-generated"
3. In-app banner on every itinerary: "This itinerary was generated by AI"
4. Feedback/report mechanism on every itinerary

Content moderation:
- Users can report inaccurate or inappropriate recommendations
- All AI output is informational only (no guarantees)
- Users are advised to "independently verify" recommendations

Test Account:
Email: reviewer@timbuktoo.ai
Password: ReviewTest2024!

Demo Flow:
1. Open app → Complete onboarding (3 screens, consent required)
2. Create account or use test account
3. Set preferences (select interests, food, budget)
4. View city recommendations (3 cities shown)
5. Generate itinerary (takes 30-60 seconds)
6. View itinerary with AI disclosure banner
7. Provide feedback or report issues
8. Settings → Privacy Policy, Terms, Delete Account

Data Deletion:
Settings → Delete My Data → Confirmation → 30-day deletion SLA
```

---

## Testing Strategy

### Unit Tests

```bash
# Install Jest
npm install --save-dev jest @testing-library/react-native

# Run tests
npm test
```

### E2E Tests (Detox)

```bash
# Install Detox
npm install --save-dev detox

# Run E2E tests
detox build -c ios.sim.debug
detox test -c ios.sim.debug
```

###

 Manual Testing Checklist

- [ ] Onboarding flow (all 3 screens)
- [ ] AI consent checkbox blocking
- [ ] Signup / Login
- [ ] Token persistence (close app, reopen → still logged in)
- [ ] Preferences save/load
- [ ] City recommendations load
- [ ] Itinerary generation (30-60s)
- [ ] AI disclosure banner visible
- [ ] Feedback submission
- [ ] Settings → Delete account
- [ ] Deep linking (if applicable)

---

## Deployment Checklist

### Pre-Submission

- [ ] Update `app.json` version to 1.0.0
- [ ] Add app icon (`assets/icon.png` - 1024x1024)
- [ ] Add splash screen (`assets/splash.png`)
- [ ] Test on real iOS device
- [ ] Test on real Android device
- [ ] Run Snyk security scan
- [ ] Privacy Policy updated (mobile addendum)
- [ ] Terms of Service updated (mobile clause)

### EAS Build

```bash
# Configure EAS
eas build:configure

# Build for iOS
eas build --platform ios --profile production

# Build for Android
eas build --platform android --profile production
```

### App Store Connect (iOS)

1. Create app in App Store Connect
2. Upload build via EAS or Xcode
3. Fill Privacy Nutrition Label (use `ios-privacy-label.json`)
4. Add app review notes (`app-review-notes.txt`)
5. Add screenshots (6.5", 5.5" required)
6. Submit for review

### Google Play Console (Android)

1. Create app in Google Play Console
2. Upload AAB via EAS or Android Studio
3. Fill Data Safety form
4. Add app content questionnaire
5. Add screenshots
6. Submit for review

---

**Timeline**: 2-3 weeks for App Store approval after submission
**Support**: mobile-support@timbuktoo.ai

---

**Document Version**: 1.0
**Last Updated**: 2024-07-16
**Owner**: Engineering Lead + Mobile Team
