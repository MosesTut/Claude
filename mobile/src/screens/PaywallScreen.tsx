import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Button, Text, Card, ActivityIndicator } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import {
  getSubscriptionOfferings,
  purchaseSubscription,
  restorePurchases,
  formatPrice,
  calculateAnnualSavings,
  isProSubscriber,
} from '../services/subscriptions';
import { PurchasesPackage } from 'react-native-purchases';

type Props = NativeStackScreenProps<RootStackParamList, 'Paywall'>;

export default function PaywallScreen({ navigation, route }: Props) {
  const { source } = route.params || { source: 'unknown' }; // Track where user came from

  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState(false);
  const [restoring, setRestoring] = useState(false);
  const [monthlyPackage, setMonthlyPackage] = useState<PurchasesPackage | null>(null);
  const [annualPackage, setAnnualPackage] = useState<PurchasesPackage | null>(null);
  const [selectedPlan, setSelectedPlan] = useState<'monthly' | 'annual'>('annual');

  useEffect(() => {
    loadOfferings();
    checkIfAlreadyPro();
  }, []);

  const checkIfAlreadyPro = async () => {
    try {
      const isPro = await isProSubscriber();
      if (isPro) {
        // User is already Pro, navigate back
        Alert.alert(
          'Already Pro',
          'You already have an active Pro subscription!',
          [{ text: 'OK', onPress: () => navigation.goBack() }]
        );
      }
    } catch (error) {
      console.error('Failed to check Pro status:', error);
    }
  };

  const loadOfferings = async () => {
    try {
      const { monthly, annual } = await getSubscriptionOfferings();
      setMonthlyPackage(monthly);
      setAnnualPackage(annual);

      if (!monthly && !annual) {
        Alert.alert(
          'Subscriptions Unavailable',
          'Unable to load subscription options. Please try again later.',
          [{ text: 'OK', onPress: () => navigation.goBack() }]
        );
      }
    } catch (error) {
      console.error('Failed to load offerings:', error);
      Alert.alert('Error', 'Failed to load subscription options.');
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async () => {
    const packageToPurchase = selectedPlan === 'monthly' ? monthlyPackage : annualPackage;

    if (!packageToPurchase) {
      Alert.alert('Error', 'Selected plan is not available.');
      return;
    }

    setPurchasing(true);

    try {
      const result = await purchaseSubscription(packageToPurchase);

      if (result.success && result.isPro) {
        Alert.alert(
          'Welcome to Pro! 🎉',
          'You now have unlimited itineraries and access to all premium features.',
          [
            {
              text: 'Get Started',
              onPress: () => navigation.replace('Preferences'),
            },
          ]
        );
      } else if (result.error) {
        if (result.error !== 'Purchase cancelled') {
          Alert.alert('Purchase Failed', result.error);
        }
      }
    } catch (error) {
      Alert.alert('Error', 'An unexpected error occurred. Please try again.');
    } finally {
      setPurchasing(false);
    }
  };

  const handleRestore = async () => {
    setRestoring(true);

    try {
      const result = await restorePurchases();

      if (result.success && result.isPro) {
        Alert.alert(
          'Purchases Restored',
          'Your Pro subscription has been restored!',
          [
            {
              text: 'Continue',
              onPress: () => navigation.replace('Preferences'),
            },
          ]
        );
      } else if (result.success && !result.isPro) {
        Alert.alert(
          'No Purchases Found',
          'We couldn\'t find any active subscriptions to restore.'
        );
      } else if (result.error) {
        Alert.alert('Restore Failed', result.error);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to restore purchases. Please try again.');
    } finally {
      setRestoring(false);
    }
  };

  const handleClose = () => {
    // Allow users to dismiss paywall (for now)
    navigation.goBack();
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#8B5CF6" />
        <Text variant="bodyLarge" style={styles.loadingText}>
          Loading subscription options...
        </Text>
      </View>
    );
  }

  const savings = calculateAnnualSavings(monthlyPackage, annualPackage);

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Header */}
        <View style={styles.header}>
          <Text variant="headlineLarge" style={styles.title}>
            Upgrade to Pro
          </Text>
          <Text variant="bodyLarge" style={styles.subtitle}>
            Unlock unlimited AI-powered travel planning
          </Text>
        </View>

        {/* Features */}
        <View style={styles.features}>
          <Feature icon="✓" text="Unlimited itineraries per month" highlight />
          <Feature icon="✓" text="Premium destinations & insights" highlight />
          <Feature icon="✓" text="Faster AI generation" highlight />
          <Feature icon="✓" text="Priority support" highlight />
          <Feature icon="✓" text="Early access to new features" highlight />
        </View>

        {/* Plans */}
        <View style={styles.plans}>
          {annualPackage && (
            <Card
              style={[styles.planCard, selectedPlan === 'annual' && styles.planCardSelected]}
              onPress={() => setSelectedPlan('annual')}
            >
              <Card.Content>
                {savings && (
                  <View style={styles.savingsBadge}>
                    <Text style={styles.savingsText}>{savings.savingsText}</Text>
                  </View>
                )}
                <Text variant="titleLarge" style={styles.planTitle}>
                  Annual Plan
                </Text>
                <Text variant="headlineMedium" style={styles.planPrice}>
                  {formatPrice(annualPackage)}
                </Text>
                <Text variant="bodySmall" style={styles.planPeriod}>
                  per year
                </Text>
                <Text variant="bodySmall" style={styles.planEquivalent}>
                  {(annualPackage.product.price / 12).toFixed(2)} {annualPackage.product.currencyCode}/month
                </Text>
              </Card.Content>
            </Card>
          )}

          {monthlyPackage && (
            <Card
              style={[styles.planCard, selectedPlan === 'monthly' && styles.planCardSelected]}
              onPress={() => setSelectedPlan('monthly')}
            >
              <Card.Content>
                <Text variant="titleLarge" style={styles.planTitle}>
                  Monthly Plan
                </Text>
                <Text variant="headlineMedium" style={styles.planPrice}>
                  {formatPrice(monthlyPackage)}
                </Text>
                <Text variant="bodySmall" style={styles.planPeriod}>
                  per month
                </Text>
              </Card.Content>
            </Card>
          )}
        </View>

        {/* CTA */}
        <Button
          mode="contained"
          onPress={handlePurchase}
          loading={purchasing}
          disabled={purchasing || restoring}
          style={styles.ctaButton}
          contentStyle={styles.ctaButtonContent}
        >
          {purchasing ? 'Processing...' : `Start Free Trial`}
        </Button>

        {/* Trial info */}
        <Text variant="bodySmall" style={styles.trialInfo}>
          7-day free trial, then {selectedPlan === 'annual' ? formatPrice(annualPackage!) : formatPrice(monthlyPackage!)} {selectedPlan === 'annual' ? 'per year' : 'per month'}
        </Text>

        {/* Restore purchases */}
        <Button
          mode="text"
          onPress={handleRestore}
          loading={restoring}
          disabled={purchasing || restoring}
          style={styles.restoreButton}
        >
          Restore Purchases
        </Button>

        {/* Terms */}
        <Text variant="bodySmall" style={styles.terms}>
          Payment will be charged to your Apple ID account at confirmation of purchase.
          Subscription automatically renews unless canceled at least 24 hours before the
          end of the current period. You can manage and cancel subscriptions in your
          App Store account settings.
        </Text>

        {/* Close button */}
        <Button mode="text" onPress={handleClose} style={styles.closeButton}>
          Maybe Later
        </Button>
      </ScrollView>
    </View>
  );
}

function Feature({ icon, text, highlight }: { icon: string; text: string; highlight?: boolean }) {
  return (
    <View style={styles.feature}>
      <Text style={styles.featureIcon}>{icon}</Text>
      <Text
        variant="bodyLarge"
        style={[styles.featureText, highlight && styles.featureTextHighlight]}
      >
        {text}
      </Text>
    </View>
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
  scrollContent: {
    paddingHorizontal: 24,
    paddingTop: 40,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    color: '#666666',
    textAlign: 'center',
  },
  features: {
    marginBottom: 32,
  },
  feature: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  featureIcon: {
    fontSize: 24,
    color: '#10B981',
    marginRight: 12,
    fontWeight: 'bold',
  },
  featureText: {
    flex: 1,
    color: '#333333',
  },
  featureTextHighlight: {
    fontWeight: '600',
    color: '#1a1a1a',
  },
  plans: {
    marginBottom: 24,
  },
  planCard: {
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#E0E0E0',
  },
  planCardSelected: {
    borderColor: '#8B5CF6',
    backgroundColor: '#F5F3FF',
  },
  savingsBadge: {
    position: 'absolute',
    top: 12,
    right: 12,
    backgroundColor: '#10B981',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
  },
  savingsText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
  planTitle: {
    fontWeight: 'bold',
    marginBottom: 8,
  },
  planPrice: {
    fontWeight: 'bold',
    color: '#8B5CF6',
  },
  planPeriod: {
    color: '#666666',
  },
  planEquivalent: {
    color: '#999999',
    marginTop: 4,
  },
  ctaButton: {
    backgroundColor: '#8B5CF6',
    marginBottom: 8,
  },
  ctaButtonContent: {
    paddingVertical: 8,
  },
  trialInfo: {
    textAlign: 'center',
    color: '#666666',
    marginBottom: 24,
  },
  restoreButton: {
    marginBottom: 24,
  },
  terms: {
    color: '#999999',
    textAlign: 'center',
    lineHeight: 18,
    marginBottom: 16,
  },
  closeButton: {
    marginTop: 8,
  },
});
