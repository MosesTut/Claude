import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { Button, Checkbox } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';

type AIDisclosureScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'AIDisclosure'>;
};

export default function AIDisclosureScreen({
  navigation,
}: AIDisclosureScreenProps) {
  const [agreed, setAgreed] = useState(false);

  const handleContinue = () => {
    if (!agreed) {
      Alert.alert(
        'Consent Required',
        'Please confirm you understand itineraries are AI-generated to continue.',
        [{ text: 'OK' }]
      );
      return;
    }
    navigation.navigate('DataUse');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.icon}>⚠️</Text>
          <Text style={styles.title}>AI Transparency</Text>
        </View>

        <View style={styles.content}>
          <Text style={styles.mainText}>
            Timbuktoo uses artificial intelligence to generate travel
            recommendations.
          </Text>

          <Text style={styles.mainText}>
            These recommendations are informational and should be independently
            verified.
          </Text>

          <View style={styles.warningBox}>
            <Text style={styles.warningTitle}>Important:</Text>
            <Text style={styles.warningText}>
              • AI-generated content may be inaccurate or incomplete
            </Text>
            <Text style={styles.warningText}>
              • Verify all recommendations before making travel decisions
            </Text>
            <Text style={styles.warningText}>
              • Timbuktoo does not guarantee accuracy, pricing, or availability
            </Text>
          </View>

          <View style={styles.checkboxContainer}>
            <Checkbox
              status={agreed ? 'checked' : 'unchecked'}
              onPress={() => setAgreed(!agreed)}
            />
            <Text
              style={styles.checkboxLabel}
              onPress={() => setAgreed(!agreed)}
            >
              I understand itineraries are AI-generated
            </Text>
          </View>
        </View>

        <View style={styles.footer}>
          <Button
            mode="contained"
            onPress={handleContinue}
            style={[styles.button, !agreed && styles.buttonDisabled]}
            contentStyle={styles.buttonContent}
            disabled={!agreed}
          >
            Agree & Continue
          </Button>

          <Button
            mode="text"
            onPress={() => navigation.goBack()}
            style={styles.backButton}
          >
            Go Back
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
    flexGrow: 1,
    padding: 24,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 32,
  },
  icon: {
    fontSize: 48,
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1a1a1a',
  },
  content: {
    flex: 1,
  },
  mainText: {
    fontSize: 16,
    color: '#333333',
    lineHeight: 24,
    marginBottom: 16,
  },
  warningBox: {
    backgroundColor: '#fff3cd',
    borderColor: '#ffc107',
    borderWidth: 1,
    borderRadius: 8,
    padding: 16,
    marginVertical: 24,
  },
  warningTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#856404',
    marginBottom: 8,
  },
  warningText: {
    fontSize: 14,
    color: '#856404',
    lineHeight: 20,
    marginBottom: 4,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
  },
  checkboxLabel: {
    fontSize: 16,
    color: '#1a1a1a',
    marginLeft: 8,
    flex: 1,
  },
  footer: {
    marginTop: 32,
  },
  button: {
    borderRadius: 8,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  backButton: {
    marginTop: 12,
  },
});
