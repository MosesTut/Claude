import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Button, Text, Card, ActivityIndicator } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import apiClient from '../services/api';
import { ENDPOINTS } from '../config/api';
import { CityRecommendation } from '../types';

type Props = NativeStackScreenProps<RootStackParamList, 'CityRecommendation'>;

export default function CityRecommendationScreen({ navigation }: Props) {
  const [cities, setCities] = useState<CityRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCity, setSelectedCity] = useState<CityRecommendation | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadCityRecommendations();
  }, []);

  const loadCityRecommendations = async () => {
    try {
      const response = await apiClient.get<{ cities: CityRecommendation[] }>(
        ENDPOINTS.GET_CITY_RECOMMENDATIONS
      );
      setCities(response.data.cities);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateItinerary = async () => {
    if (!selectedCity) {
      Alert.alert('No City Selected', 'Please select a city first');
      return;
    }

    setGenerating(true);

    try {
      const response = await apiClient.post(ENDPOINTS.GENERATE_ITINERARY, {
        city_name: selectedCity.city_name,
        country: selectedCity.country,
        trip_length_days: 3, // Will be replaced with actual trip length from preferences
      });

      // Navigate to Itinerary screen
      navigation.navigate('Itinerary', { itineraryId: response.data.id });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to generate itinerary';

      // Check if it's a rate limit error
      if (error.response?.status === 403) {
        Alert.alert(
          'Free Tier Limit Reached',
          errorMessage,
          [
            { text: 'OK' },
            {
              text: 'Upgrade to Pro',
              onPress: () => {
                navigation.navigate('Paywall', { source: 'rate_limit' });
              },
            },
          ]
        );
      } else {
        Alert.alert('Error', errorMessage);
      }
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#8B5CF6" />
        <Text variant="bodyLarge" style={styles.loadingText}>
          Finding perfect cities for you...
        </Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text variant="headlineMedium" style={styles.title}>
        Recommended Cities
      </Text>

      <Text variant="bodyMedium" style={styles.subtitle}>
        Based on your preferences, we recommend these destinations:
      </Text>

      {cities.map((city, index) => (
        <Card
          key={index}
          style={[styles.card, selectedCity?.city_name === city.city_name && styles.cardSelected]}
          onPress={() => setSelectedCity(city)}
        >
          <Card.Content>
            <Text variant="titleLarge" style={styles.cityName}>
              {city.city_name}, {city.country}
            </Text>
            <Text variant="bodyMedium" style={styles.reasoning}>
              {city.reasoning}
            </Text>
            {city.match_score && (
              <Text variant="bodySmall" style={styles.matchScore}>
                Match Score: {Math.round(city.match_score * 100)}%
              </Text>
            )}
          </Card.Content>
        </Card>
      ))}

      <Button
        mode="contained"
        onPress={handleGenerateItinerary}
        loading={generating}
        disabled={!selectedCity || generating}
        style={styles.button}
        contentStyle={styles.buttonContent}
      >
        {generating ? 'Generating Itinerary (30-60s)...' : 'Generate Itinerary'}
      </Button>

      <Button mode="text" onPress={() => navigation.goBack()} style={styles.backButton}>
        Change Preferences
      </Button>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
  },
  loadingText: {
    marginTop: 16,
    color: '#666666',
  },
  content: {
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 16,
  },
  subtitle: {
    marginBottom: 24,
    color: '#666666',
  },
  card: {
    marginBottom: 16,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  cardSelected: {
    borderColor: '#8B5CF6',
    backgroundColor: '#F3F4F6',
  },
  cityName: {
    fontWeight: 'bold',
    marginBottom: 12,
  },
  reasoning: {
    color: '#666666',
    lineHeight: 22,
  },
  matchScore: {
    marginTop: 12,
    color: '#8B5CF6',
    fontWeight: '600',
  },
  button: {
    marginTop: 32,
    backgroundColor: '#8B5CF6',
  },
  buttonContent: {
    paddingVertical: 8,
  },
  backButton: {
    marginTop: 16,
  },
});
