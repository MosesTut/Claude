import React from 'react';
import { View, StyleSheet, Image } from 'react-native';
import { Button, Text } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';

type Props = NativeStackScreenProps<RootStackParamList, 'OnboardingWelcome'>;

export default function OnboardingWelcomeScreen({ navigation }: Props) {
  return (
    <View style={styles.container}>
      <Image
        source={require('../../assets/icon.png')}
        style={styles.image}
        resizeMode="contain"
      />

      <View style={styles.content}>
        <Text variant="headlineLarge" style={styles.title}>
          Welcome to Timbuktoo
        </Text>

        <Text variant="bodyLarge" style={styles.description}>
          Your personal AI travel concierge. Get personalized trip itineraries
          tailored to your interests, budget, and travel style.
        </Text>

        <View style={styles.features}>
          <Text variant="bodyMedium" style={styles.feature}>
            ✓ AI-powered city recommendations
          </Text>
          <Text variant="bodyMedium" style={styles.feature}>
            ✓ Day-by-day itineraries
          </Text>
          <Text variant="bodyMedium" style={styles.feature}>
            ✓ Restaurant and activity suggestions
          </Text>
          <Text variant="bodyMedium" style={styles.feature}>
            ✓ Personalized to your preferences
          </Text>
        </View>

        <Button
          mode="contained"
          onPress={() => navigation.navigate('AIDisclosure')}
          style={styles.button}
          contentStyle={styles.buttonContent}
        >
          Get Started
        </Button>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  image: {
    width: '100%',
    height: 250,
    marginTop: 60,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 40,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 16,
    textAlign: 'center',
  },
  description: {
    textAlign: 'center',
    marginBottom: 32,
    color: '#666666',
  },
  features: {
    marginBottom: 40,
  },
  feature: {
    marginBottom: 12,
    paddingLeft: 8,
  },
  button: {
    marginTop: 'auto',
    marginBottom: 32,
    backgroundColor: '#8B5CF6',
  },
  buttonContent: {
    paddingVertical: 8,
  },
});
