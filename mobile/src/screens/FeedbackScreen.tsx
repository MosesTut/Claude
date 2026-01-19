import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { Button, TextInput, RadioButton } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../../App';
import * as SecureStore from 'expo-secure-store';
import { feedbackAPI } from '../api/feedback';

type FeedbackScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Feedback'>;
  route: RouteProp<RootStackParamList, 'Feedback'>;
};

export default function FeedbackScreen({
  navigation,
  route,
}: FeedbackScreenProps) {
  const { itineraryId } = route.params;
  const [rating, setRating] = useState<'helpful' | 'not-helpful' | null>(null);
  const [reportType, setReportType] = useState<string>('');
  const [comments, setComments] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!rating && !reportType) {
      Alert.alert('Error', 'Please provide feedback or report an issue');
      return;
    }

    setLoading(true);

    try {
      const token = await SecureStore.getItemAsync('authToken');
      if (!token) throw new Error('Not authenticated');

      await feedbackAPI.submitFeedback(token, {
        itineraryId,
        rating,
        reportType,
        comments,
      });

      Alert.alert(
        'Thank You',
        'Your feedback helps us improve recommendations.',
        [
          {
            text: 'OK',
            onPress: () => navigation.navigate('Preferences'),
          },
        ]
      );
    } catch (error: any) {
      Alert.alert('Error', 'Failed to submit feedback. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>How was your itinerary?</Text>
          <Text style={styles.subtitle}>
            Your feedback helps improve AI recommendations
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Overall Rating</Text>
          <View style={styles.ratingContainer}>
            <Button
              mode={rating === 'helpful' ? 'contained' : 'outlined'}
              onPress={() => setRating('helpful')}
              icon="thumb-up"
              style={styles.ratingButton}
            >
              👍 Helpful
            </Button>
            <Button
              mode={rating === 'not-helpful' ? 'contained' : 'outlined'}
              onPress={() => setRating('not-helpful')}
              icon="thumb-down"
              style={styles.ratingButton}
            >
              👎 Not Helpful
            </Button>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>⚠️ Report an Issue</Text>
          <Text style={styles.sectionSubtitle}>
            Required for AI-generated content apps
          </Text>

          <RadioButton.Group
            onValueChange={(value) => setReportType(value)}
            value={reportType}
          >
            <View style={styles.radioItem}>
              <RadioButton value="inaccurate" />
              <Text style={styles.radioLabel}>Inaccurate information</Text>
            </View>
            <View style={styles.radioItem}>
              <RadioButton value="inappropriate" />
              <Text style={styles.radioLabel}>Inappropriate content</Text>
            </View>
            <View style={styles.radioItem}>
              <RadioButton value="missing" />
              <Text style={styles.radioLabel}>
                Missing key information
              </Text>
            </View>
            <View style={styles.radioItem}>
              <RadioButton value="other" />
              <Text style={styles.radioLabel}>Other issue</Text>
            </View>
          </RadioButton.Group>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Additional Comments (Optional)</Text>
          <TextInput
            mode="outlined"
            multiline
            numberOfLines={4}
            value={comments}
            onChangeText={setComments}
            placeholder="Tell us more about your experience..."
            style={styles.textArea}
          />
        </View>

        <View style={styles.footer}>
          <Button
            mode="contained"
            onPress={handleSubmit}
            loading={loading}
            disabled={loading || (!rating && !reportType)}
            style={styles.submitButton}
            contentStyle={styles.buttonContent}
          >
            Submit Feedback
          </Button>

          <Button
            mode="text"
            onPress={() => navigation.goBack()}
            style={styles.skipButton}
          >
            Skip for Now
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
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  sectionSubtitle: {
    fontSize: 12,
    color: '#999999',
    marginBottom: 12,
  },
  ratingContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  ratingButton: {
    flex: 1,
  },
  radioItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  radioLabel: {
    fontSize: 16,
    color: '#1a1a1a',
    marginLeft: 8,
  },
  textArea: {
    marginTop: 8,
  },
  footer: {
    marginTop: 16,
  },
  submitButton: {
    borderRadius: 8,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  skipButton: {
    marginTop: 12,
  },
});
