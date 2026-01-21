import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Button, Text, Chip, SegmentedButtons, TextInput } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import apiClient from '../services/api';
import { ENDPOINTS } from '../config/api';
import { Preferences } from '../types';
import { formatErrorAlert } from '../utils/errors';
import { validatePreferencesForm } from '../utils/validation';

type Props = NativeStackScreenProps<RootStackParamList, 'Preferences'>;

const INTEREST_OPTIONS = [
  'Culture & Museums',
  'Food & Dining',
  'Nature & Outdoors',
  'History',
  'Shopping',
  'Nightlife',
  'Architecture',
  'Adventure',
];

const FOOD_OPTIONS = ['Vegetarian', 'Vegan', 'Halal', 'Kosher', 'Gluten-Free', 'No Restrictions'];

export default function PreferencesScreen({ navigation }: Props) {
  const [interests, setInterests] = useState<string[]>([]);
  const [foodPreferences, setFoodPreferences] = useState<string[]>([]);
  const [budget, setBudget] = useState<'budget' | 'mid-range' | 'luxury'>('mid-range');
  const [pace, setPace] = useState<'relaxed' | 'moderate' | 'packed'>('moderate');
  const [tripLength, setTripLength] = useState('3');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPreferences();
  }, []);

  const loadPreferences = async () => {
    try {
      const response = await apiClient.get<Preferences>(ENDPOINTS.GET_PREFERENCES);
      if (response.data) {
        setInterests(response.data.interests || []);
        setFoodPreferences(response.data.food_preferences || []);
        setBudget(response.data.budget_level || 'mid-range');
        setPace(response.data.pace || 'moderate');
        setTripLength(String(response.data.trip_length_days || 3));
      }
    } catch (error) {
      console.error('Failed to load preferences:', error);
    }
  };

  const toggleInterest = (interest: string) => {
    if (interests.includes(interest)) {
      setInterests(interests.filter((i) => i !== interest));
    } else {
      setInterests([...interests, interest]);
    }
  };

  const toggleFoodPreference = (pref: string) => {
    if (foodPreferences.includes(pref)) {
      setFoodPreferences(foodPreferences.filter((p) => p !== pref));
    } else {
      setFoodPreferences([...foodPreferences, pref]);
    }
  };

  const handleSaveAndContinue = async () => {
    // Validate form before submission
    const validation = validatePreferencesForm({
      interests,
      foodPreferences,
      tripLength,
      budget,
      pace,
    });

    if (!validation.isValid) {
      Alert.alert('Validation Error', validation.error || 'Please check your input');
      return;
    }

    setLoading(true);

    try {
      const preferences: Preferences = {
        interests,
        food_preferences: foodPreferences,
        budget_level: budget,
        pace,
        trip_length_days: parseInt(tripLength),
      };

      await apiClient.post(ENDPOINTS.SAVE_PREFERENCES, preferences);

      // Navigate to City Recommendations
      navigation.navigate('CityRecommendation');
    } catch (error: any) {
      const { title, message } = formatErrorAlert(error);
      Alert.alert(title, message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text variant="headlineMedium" style={styles.title}>
        Tell Us Your Preferences
      </Text>

      {/* Interests */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        What are you interested in?
      </Text>
      <View style={styles.chipContainer}>
        {INTEREST_OPTIONS.map((interest) => (
          <Chip
            key={interest}
            selected={interests.includes(interest)}
            onPress={() => toggleInterest(interest)}
            style={styles.chip}
            mode="outlined"
            selectedColor="#8B5CF6"
          >
            {interest}
          </Chip>
        ))}
      </View>

      {/* Food Preferences */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Food Preferences
      </Text>
      <View style={styles.chipContainer}>
        {FOOD_OPTIONS.map((pref) => (
          <Chip
            key={pref}
            selected={foodPreferences.includes(pref)}
            onPress={() => toggleFoodPreference(pref)}
            style={styles.chip}
            mode="outlined"
            selectedColor="#8B5CF6"
          >
            {pref}
          </Chip>
        ))}
      </View>

      {/* Budget */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Budget Level
      </Text>
      <SegmentedButtons
        value={budget}
        onValueChange={(value) => setBudget(value as any)}
        buttons={[
          { value: 'budget', label: 'Budget' },
          { value: 'mid-range', label: 'Mid-Range' },
          { value: 'luxury', label: 'Luxury' },
        ]}
        style={styles.segmentedButtons}
      />

      {/* Pace */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Travel Pace
      </Text>
      <SegmentedButtons
        value={pace}
        onValueChange={(value) => setPace(value as any)}
        buttons={[
          { value: 'relaxed', label: 'Relaxed' },
          { value: 'moderate', label: 'Moderate' },
          { value: 'packed', label: 'Packed' },
        ]}
        style={styles.segmentedButtons}
      />

      {/* Trip Length */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Trip Length (days)
      </Text>
      <TextInput
        value={tripLength}
        onChangeText={setTripLength}
        keyboardType="number-pad"
        mode="outlined"
        style={styles.input}
        placeholder="e.g., 3"
      />

      <Button
        mode="contained"
        onPress={handleSaveAndContinue}
        loading={loading}
        disabled={loading}
        style={styles.button}
        contentStyle={styles.buttonContent}
      >
        Get City Recommendations
      </Button>

      <Button
        mode="text"
        onPress={() => navigation.navigate('Settings')}
        style={styles.settingsButton}
      >
        Settings
      </Button>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  content: {
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 32,
  },
  sectionTitle: {
    fontWeight: 'bold',
    marginBottom: 16,
    marginTop: 24,
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chip: {
    marginBottom: 8,
  },
  segmentedButtons: {
    marginBottom: 16,
  },
  input: {
    marginBottom: 16,
  },
  button: {
    marginTop: 32,
    backgroundColor: '#8B5CF6',
  },
  buttonContent: {
    paddingVertical: 8,
  },
  settingsButton: {
    marginTop: 16,
  },
});
