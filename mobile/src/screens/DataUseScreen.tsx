import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Linking,
} from 'react-native';
import { Button } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';

type DataUseScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'DataUse'>;
};

export default function DataUseScreen({ navigation }: DataUseScreenProps) {
  const openPrivacyPolicy = () => {
    Linking.openURL('https://timbuktoo.ai/privacy');
  };

  const openTermsOfService = () => {
    Linking.openURL('https://timbuktoo.ai/terms');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.icon}>🔒</Text>
          <Text style={styles.title}>Your Privacy Matters</Text>
        </View>

        <View style={styles.content}>
          <Text style={styles.mainText}>
            We use your preferences to personalize recommendations. You can
            delete your data at any time.
          </Text>

          <View style={styles.dataSection}>
            <DataItem
              title="What We Collect"
              description="Travel preferences, destination interests, and account information"
            />
            <DataItem
              title="How We Use It"
              description="To personalize AI-generated itineraries and improve recommendations"
            />
            <DataItem
              title="Your Control"
              description="Delete your data anytime from Settings or by contacting support"
            />
          </View>

          <View style={styles.linksSection}>
            <Text style={styles.linksTitle}>Learn More:</Text>
            <Button
              mode="outlined"
              onPress={openPrivacyPolicy}
              style={styles.linkButton}
            >
              Privacy Policy
            </Button>
            <Button
              mode="outlined"
              onPress={openTermsOfService}
              style={styles.linkButton}
            >
              Terms of Service
            </Button>
          </View>
        </View>

        <View style={styles.footer}>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('Auth', { mode: 'signup' })}
            style={styles.button}
            contentStyle={styles.buttonContent}
          >
            Get Started
          </Button>

          <Button
            mode="text"
            onPress={() => navigation.navigate('Auth', { mode: 'login' })}
            style={styles.loginButton}
          >
            Already have an account? Log in
          </Button>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function DataItem({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <View style={styles.dataItem}>
      <Text style={styles.dataItemTitle}>{title}</Text>
      <Text style={styles.dataItemDescription}>{description}</Text>
    </View>
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
    marginBottom: 24,
    textAlign: 'center',
  },
  dataSection: {
    gap: 20,
    marginBottom: 32,
  },
  dataItem: {
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    padding: 16,
  },
  dataItemTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  dataItemDescription: {
    fontSize: 14,
    color: '#666666',
    lineHeight: 20,
  },
  linksSection: {
    marginTop: 16,
  },
  linksTitle: {
    fontSize: 14,
    color: '#666666',
    marginBottom: 12,
  },
  linkButton: {
    marginBottom: 8,
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
  loginButton: {
    marginTop: 12,
  },
});
