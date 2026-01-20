import React, { useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import { ActivityIndicator, Text } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import { getAuthToken } from '../services/api';

type Props = NativeStackScreenProps<RootStackParamList, 'Splash'>;

export default function SplashScreen({ navigation }: Props) {
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = await getAuthToken();

      // Simulate loading time
      await new Promise(resolve => setTimeout(resolve, 1500));

      if (token) {
        // User is logged in, go to Preferences
        navigation.replace('Preferences');
      } else {
        // User is not logged in, go to Onboarding
        navigation.replace('Onboarding');
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      navigation.replace('Onboarding');
    }
  };

  return (
    <View style={styles.container}>
      <Text variant="displaySmall" style={styles.appName}>
        Timbuktoo
      </Text>
      <Text variant="titleMedium" style={styles.tagline}>
        AI-Powered Travel Planning
      </Text>
      <ActivityIndicator size="large" color="#8B5CF6" style={styles.loader} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#8B5CF6',
    alignItems: 'center',
    justifyContent: 'center',
  },
  appName: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  tagline: {
    color: '#FFFFFF',
    opacity: 0.9,
    marginBottom: 40,
  },
  loader: {
    marginTop: 20,
  },
});
