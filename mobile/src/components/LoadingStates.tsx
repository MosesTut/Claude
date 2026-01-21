import React from 'react';
import { View, StyleSheet } from 'react-native';
import { ActivityIndicator, Text, Card } from 'react-native-paper';

// Full screen loading with message
export function FullScreenLoading({ message }: { message?: string }) {
  return (
    <View style={styles.fullScreenContainer}>
      <ActivityIndicator size="large" color="#8B5CF6" />
      {message && (
        <Text variant="bodyLarge" style={styles.loadingMessage}>
          {message}
        </Text>
      )}
    </View>
  );
}

// Skeleton for city cards
export function CityCardSkeleton() {
  return (
    <Card style={styles.skeletonCard}>
      <Card.Content>
        <View style={[styles.skeleton, styles.skeletonTitle]} />
        <View style={[styles.skeleton, styles.skeletonText]} />
        <View style={[styles.skeleton, styles.skeletonText, { width: '70%' }]} />
        <View style={[styles.skeleton, styles.skeletonScore]} />
      </Card.Content>
    </Card>
  );
}

// Skeleton for itinerary day card
export function ItineraryDaySkeleton() {
  return (
    <Card style={styles.skeletonCard}>
      <Card.Content>
        <View style={[styles.skeleton, styles.skeletonTitle]} />

        {/* Morning section */}
        <View style={styles.skeletonSection}>
          <View style={[styles.skeleton, styles.skeletonSmall]} />
          <View style={[styles.skeleton, styles.skeletonText]} />
          <View style={[styles.skeleton, styles.skeletonText, { width: '60%' }]} />
        </View>

        {/* Lunch section */}
        <View style={styles.skeletonSection}>
          <View style={[styles.skeleton, styles.skeletonSmall]} />
          <View style={[styles.skeleton, styles.skeletonText, { width: '80%' }]} />
        </View>

        {/* Afternoon section */}
        <View style={styles.skeletonSection}>
          <View style={[styles.skeleton, styles.skeletonSmall]} />
          <View style={[styles.skeleton, styles.skeletonText]} />
        </View>
      </Card.Content>
    </Card>
  );
}

// Loading button state
export function LoadingButton({
  loading,
  text,
  loadingText,
  onPress,
  disabled,
  style,
}: {
  loading: boolean;
  text: string;
  loadingText: string;
  onPress: () => void;
  disabled?: boolean;
  style?: any;
}) {
  return (
    <View style={style}>
      <ActivityIndicator
        animating={loading}
        size="small"
        color="#8B5CF6"
        style={{ opacity: loading ? 1 : 0, height: loading ? 20 : 0 }}
      />
      <Text style={styles.buttonLoadingText}>
        {loading ? loadingText : text}
      </Text>
    </View>
  );
}

// AI generation progress indicator
export function AIGenerationProgress({
  stage,
  estimatedTime,
}: {
  stage: 'starting' | 'analyzing' | 'generating' | 'finalizing';
  estimatedTime?: number;
}) {
  const stageMessages = {
    starting: 'Analyzing your preferences...',
    analyzing: 'Finding perfect destinations...',
    generating: 'Creating your personalized itinerary...',
    finalizing: 'Adding final touches...',
  };

  const progress = {
    starting: 0.25,
    analyzing: 0.5,
    generating: 0.75,
    finalizing: 0.9,
  };

  return (
    <View style={styles.aiProgressContainer}>
      <ActivityIndicator size="large" color="#8B5CF6" />

      <Text variant="titleMedium" style={styles.aiProgressTitle}>
        {stageMessages[stage]}
      </Text>

      {/* Progress bar */}
      <View style={styles.progressBarContainer}>
        <View style={[styles.progressBar, { width: `${progress[stage] * 100}%` }]} />
      </View>

      {estimatedTime && (
        <Text variant="bodySmall" style={styles.aiProgressTime}>
          Estimated time: {estimatedTime} seconds
        </Text>
      )}

      <Text variant="bodySmall" style={styles.aiProgressHint}>
        💡 Tip: We're using AI to create a unique itinerary just for you
      </Text>
    </View>
  );
}

// Empty state component
export function EmptyState({
  icon,
  title,
  message,
  actionLabel,
  onAction,
}: {
  icon: string;
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}) {
  return (
    <View style={styles.emptyStateContainer}>
      <Text style={styles.emptyStateIcon}>{icon}</Text>
      <Text variant="titleLarge" style={styles.emptyStateTitle}>
        {title}
      </Text>
      <Text variant="bodyMedium" style={styles.emptyStateMessage}>
        {message}
      </Text>
      {actionLabel && onAction && (
        <Text
          variant="labelLarge"
          style={styles.emptyStateAction}
          onPress={onAction}
        >
          {actionLabel}
        </Text>
      )}
    </View>
  );
}

// Retry component for errors
export function RetryView({
  title,
  message,
  onRetry,
}: {
  title: string;
  message: string;
  onRetry: () => void;
}) {
  return (
    <View style={styles.retryContainer}>
      <Text style={styles.retryIcon}>⚠️</Text>
      <Text variant="titleLarge" style={styles.retryTitle}>
        {title}
      </Text>
      <Text variant="bodyMedium" style={styles.retryMessage}>
        {message}
      </Text>
      <Text
        variant="labelLarge"
        style={styles.retryButton}
        onPress={onRetry}
      >
        Try Again
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  // Full screen loading
  fullScreenContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 24,
  },
  loadingMessage: {
    marginTop: 16,
    color: '#666666',
    textAlign: 'center',
  },

  // Skeleton styles
  skeletonCard: {
    marginHorizontal: 24,
    marginBottom: 16,
  },
  skeleton: {
    backgroundColor: '#E0E0E0',
    borderRadius: 4,
  },
  skeletonTitle: {
    height: 24,
    width: '60%',
    marginBottom: 12,
  },
  skeletonText: {
    height: 16,
    width: '100%',
    marginBottom: 8,
  },
  skeletonSmall: {
    height: 14,
    width: '40%',
    marginBottom: 8,
  },
  skeletonScore: {
    height: 12,
    width: '30%',
    marginTop: 8,
  },
  skeletonSection: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F0F0F0',
  },

  // Loading button
  buttonLoadingText: {
    textAlign: 'center',
    marginTop: 8,
  },

  // AI generation progress
  aiProgressContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 32,
    backgroundColor: '#FFFFFF',
  },
  aiProgressTitle: {
    marginTop: 24,
    marginBottom: 16,
    textAlign: 'center',
    fontWeight: '600',
  },
  progressBarContainer: {
    width: '100%',
    height: 4,
    backgroundColor: '#E0E0E0',
    borderRadius: 2,
    overflow: 'hidden',
    marginVertical: 16,
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#8B5CF6',
    borderRadius: 2,
  },
  aiProgressTime: {
    color: '#999999',
    marginBottom: 8,
  },
  aiProgressHint: {
    color: '#8B5CF6',
    textAlign: 'center',
    marginTop: 24,
    fontStyle: 'italic',
  },

  // Empty state
  emptyStateContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 32,
    backgroundColor: '#FFFFFF',
  },
  emptyStateIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyStateTitle: {
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  emptyStateMessage: {
    color: '#666666',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 22,
  },
  emptyStateAction: {
    color: '#8B5CF6',
    fontWeight: '600',
    textDecorationLine: 'underline',
  },

  // Retry view
  retryContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 32,
    backgroundColor: '#FFFFFF',
  },
  retryIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  retryTitle: {
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
  },
  retryMessage: {
    color: '#666666',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 22,
  },
  retryButton: {
    color: '#FFFFFF',
    backgroundColor: '#8B5CF6',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    fontWeight: '600',
    overflow: 'hidden',
  },
});
