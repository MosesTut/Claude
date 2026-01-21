import React, { useState } from 'react';
import {
  View,
  SafeAreaView,
  StyleSheet,
  ScrollView,
  Alert,
  Linking,
} from 'react-native';
import { List, Button, Dialog, Portal, Text, Paragraph } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../../App';
import apiClient, { clearAuthToken } from '../services/api';
import { ENDPOINTS } from '../config/api';

type SettingsScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Settings'>;
};

export default function SettingsScreen({ navigation }: SettingsScreenProps) {
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleLogout = async () => {
    Alert.alert('Log Out', 'Are you sure you want to log out?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Log Out',
        style: 'destructive',
        onPress: async () => {
          try {
            await clearAuthToken();
            navigation.reset({
              index: 0,
              routes: [{ name: 'Onboarding' }],
            });
          } catch (error) {
            Alert.alert('Error', 'Failed to log out. Please try again.');
          }
        },
      },
    ]);
  };

  const handleDeleteAccount = async () => {
    setDeleteDialogVisible(false);
    setDeleting(true);

    try {
      await apiClient.delete(ENDPOINTS.DELETE_ACCOUNT);

      // Clear local data
      await clearAuthToken();

      Alert.alert(
        'Account Deleted',
        'Your account and all data have been deleted. This action cannot be undone.',
        [
          {
            text: 'OK',
            onPress: () =>
              navigation.reset({
                index: 0,
                routes: [{ name: 'Onboarding' }],
              }),
          },
        ]
      );
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to delete account. Please contact support.');
    } finally {
      setDeleting(false);
    }
  };

  const openURL = (url: string) => {
    Linking.openURL(url);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Settings</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>
          <List.Item
            title="Email"
            description="[email from API]"
            left={(props) => <List.Icon {...props} icon="email" />}
          />
          <List.Item
            title="Log Out"
            onPress={handleLogout}
            left={(props) => <List.Icon {...props} icon="logout" />}
            right={(props) => <List.Icon {...props} icon="chevron-right" />}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Legal</Text>
          <List.Item
            title="Privacy Policy"
            onPress={() => openURL('https://timbuktoo.ai/privacy')}
            left={(props) => <List.Icon {...props} icon="shield-lock" />}
            right={(props) => <List.Icon {...props} icon="open-in-new" />}
          />
          <List.Item
            title="Terms of Service"
            onPress={() => openURL('https://timbuktoo.ai/terms')}
            left={(props) => <List.Icon {...props} icon="file-document" />}
            right={(props) => <List.Icon {...props} icon="open-in-new" />}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          <List.Item
            title="Contact Support"
            description="support@timbuktoo.ai"
            onPress={() => openURL('mailto:support@timbuktoo.ai')}
            left={(props) => <List.Icon {...props} icon="help-circle" />}
            right={(props) => <List.Icon {...props} icon="open-in-new" />}
          />
          <List.Item
            title="Report a Bug"
            onPress={() => openURL('mailto:support@timbuktoo.ai?subject=Bug Report')}
            left={(props) => <List.Icon {...props} icon="bug" />}
            right={(props) => <List.Icon {...props} icon="open-in-new" />}
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          <List.Item
            title="App Version"
            description="1.0.0"
            left={(props) => <List.Icon {...props} icon="information" />}
          />
          <List.Item
            title="AI Disclosure"
            description="This app uses AI to generate recommendations"
            left={(props) => <List.Icon {...props} icon="robot" />}
          />
        </View>

        <View style={styles.dangerSection}>
          <Text style={styles.dangerTitle}>Danger Zone</Text>
          <Button
            mode="outlined"
            onPress={() => setDeleteDialogVisible(true)}
            style={styles.deleteButton}
            textColor="#d32f2f"
          >
            Delete My Data
          </Button>
          <Text style={styles.deleteHint}>
            Permanently delete your account and all data. This cannot be undone.
          </Text>
        </View>
      </ScrollView>

      {/* Delete Confirmation Dialog */}
      <Portal>
        <Dialog
          visible={deleteDialogVisible}
          onDismiss={() => setDeleteDialogVisible(false)}
        >
          <Dialog.Title>Delete Account?</Dialog.Title>
          <Dialog.Content>
            <Paragraph>
              This will permanently delete:
            </Paragraph>
            <Paragraph style={styles.deleteList}>
              • Your account
              {'\n'}• All preferences
              {'\n'}• All saved itineraries
              {'\n'}• All feedback
            </Paragraph>
            <Paragraph style={styles.deleteWarning}>
              This action cannot be undone. Deletion will be completed within 30 days.
            </Paragraph>
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setDeleteDialogVisible(false)}>Cancel</Button>
            <Button
              onPress={handleDeleteAccount}
              textColor="#d32f2f"
              loading={deleting}
              disabled={deleting}
            >
              Delete Everything
            </Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  scrollContent: {
    paddingBottom: 40,
  },
  header: {
    padding: 24,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a1a',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666666',
    textTransform: 'uppercase',
    paddingHorizontal: 24,
    marginBottom: 8,
  },
  dangerSection: {
    marginTop: 32,
    paddingHorizontal: 24,
    paddingTop: 24,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
  },
  dangerTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#d32f2f',
    textTransform: 'uppercase',
    marginBottom: 12,
  },
  deleteButton: {
    borderColor: '#d32f2f',
  },
  deleteHint: {
    fontSize: 12,
    color: '#999999',
    marginTop: 8,
    lineHeight: 18,
  },
  deleteList: {
    marginVertical: 12,
    lineHeight: 24,
  },
  deleteWarning: {
    marginTop: 12,
    color: '#d32f2f',
    fontWeight: '500',
  },
});
