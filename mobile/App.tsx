import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Provider as PaperProvider } from 'react-native-paper';
import * as SecureStore from 'expo-secure-store';

// Screens
import SplashScreen from './src/screens/SplashScreen';
import OnboardingScreen from './src/screens/OnboardingScreen';
import AIDisclosureScreen from './src/screens/AIDisclosureScreen';
import DataUseScreen from './src/screens/DataUseScreen';
import AuthScreen from './src/screens/AuthScreen';
import PreferencesScreen from './src/screens/PreferencesScreen';
import CityRecommendationScreen from './src/screens/CityRecommendationScreen';
import ItineraryScreen from './src/screens/ItineraryScreen';
import FeedbackScreen from './src/screens/FeedbackScreen';
import SettingsScreen from './src/screens/SettingsScreen';

// Types
export type RootStackParamList = {
  Splash: undefined;
  Onboarding: undefined;
  AIDisclosure: undefined;
  DataUse: undefined;
  Auth: { mode?: 'login' | 'signup' };
  Preferences: undefined;
  CityRecommendation: undefined;
  Itinerary: { itineraryId: string };
  Feedback: { itineraryId: string };
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  const [isFirstLaunch, setIsFirstLaunch] = useState<boolean | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    checkFirstLaunch();
    checkAuthentication();
  }, []);

  const checkFirstLaunch = async () => {
    try {
      const hasLaunched = await SecureStore.getItemAsync('hasLaunched');
      if (hasLaunched === null) {
        setIsFirstLaunch(true);
        await SecureStore.setItemAsync('hasLaunched', 'true');
      } else {
        setIsFirstLaunch(false);
      }
    } catch (error) {
      console.error('Error checking first launch:', error);
      setIsFirstLaunch(true);
    }
  };

  const checkAuthentication = async () => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      setIsAuthenticated(!!token);
    } catch (error) {
      console.error('Error checking authentication:', error);
      setIsAuthenticated(false);
    }
  };

  if (isFirstLaunch === null || isAuthenticated === null) {
    return <SplashScreen />;
  }

  return (
    <PaperProvider>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName={
            isFirstLaunch
              ? 'Onboarding'
              : isAuthenticated
              ? 'Preferences'
              : 'Auth'
          }
          screenOptions={{
            headerShown: false,
            animation: 'slide_from_right',
          }}
        >
          <Stack.Screen name="Splash" component={SplashScreen} />
          <Stack.Screen name="Onboarding" component={OnboardingScreen} />
          <Stack.Screen name="AIDisclosure" component={AIDisclosureScreen} />
          <Stack.Screen name="DataUse" component={DataUseScreen} />
          <Stack.Screen name="Auth" component={AuthScreen} />
          <Stack.Screen name="Preferences" component={PreferencesScreen} />
          <Stack.Screen
            name="CityRecommendation"
            component={CityRecommendationScreen}
          />
          <Stack.Screen name="Itinerary" component={ItineraryScreen} />
          <Stack.Screen name="Feedback" component={FeedbackScreen} />
          <Stack.Screen name="Settings" component={SettingsScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
}
