import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import { Button, TextInput, RadioButton, Text } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../../App';
import apiClient from '../services/api';
import { ENDPOINTS } from '../config/api';
import { FeedbackType } from '../types';

type FeedbackScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Feedback'>;
  route: RouteProp<RootStackParamList, 'Feedback'>;
};

export default function FeedbackScreen({
  navigation,
  route,
}: FeedbackScreenProps) {
  const { itineraryId } = route.params;
  const [feedbackType, setFeedbackType] = useState<FeedbackType>('other');
  const [comments, setComments] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);

    try {
      await apiClient.post(ENDPOINTS.SUBMIT_FEEDBACK, {
        itinerary_id: itineraryId,
        feedback_type: feedbackType,
        comments: comments || undefined,
      });

      Alert.alert(
        'Thank You',
        'Your feedback has been submitted and will be reviewed within 48 hours.',
        [
          {
            text: 'OK',
            onPress: () => navigation.goBack(),
          },
        ]
      );
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to submit feedback');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      <Text variant="headlineMedium" style={styles.title}>
        Report an Issue
      </Text>

      <Text variant="bodyMedium" style={styles.subtitle}>
        Help us improve by reporting issues with AI-generated content
      </Text>

      <View style={styles.section}>
        <Text variant="titleMedium" style={styles.sectionTitle}>
          What's the issue?
        </Text>

        <RadioButton.Group
          onValueChange={value => setFeedbackType(value as FeedbackType)}
          value={feedbackType}
        >
          <RadioButton.Item label="Inaccurate information" value="inaccurate" />
          <RadioButton.Item label="Inappropriate content" value="inappropriate" />
          <RadioButton.Item label="Missing information" value="missing_information" />
          <RadioButton.Item label="Other" value="other" />
        </RadioButton.Group>
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
