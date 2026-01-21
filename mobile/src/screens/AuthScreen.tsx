import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { TextInput, Button, SegmentedButtons, Text } from 'react-native-paper';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../../App';
import apiClient, { setAuthToken } from '../services/api';
import { ENDPOINTS } from '../config/api';
import { AuthResponse } from '../types';
import { formatErrorAlert } from '../utils/errors';
import { validateSignupForm, validateLoginForm } from '../utils/validation';

type AuthScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Auth'>;
  route: RouteProp<RootStackParamList, 'Auth'>;
};

export default function AuthScreen({ navigation, route }: AuthScreenProps) {
  const initialMode = route.params?.mode || 'signup';
  const [mode, setMode] = useState<'login' | 'signup'>(initialMode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAuth = async () => {
    // Validate form before submission
    const validation = mode === 'signup'
      ? validateSignupForm({ email, password, confirmPassword: password })
      : validateLoginForm({ email, password });

    if (!validation.isValid) {
      Alert.alert('Validation Error', validation.error || 'Please check your input');
      return;
    }

    setLoading(true);

    try {
      const endpoint = mode === 'signup' ? ENDPOINTS.SIGNUP : ENDPOINTS.LOGIN;
      const payload =
        mode === 'signup'
          ? {
              email,
              password,
              ai_disclosure_accepted: true,
              data_use_accepted: true,
            }
          : {
              email,
              password,
            };

      const response = await apiClient.post<AuthResponse>(endpoint, payload);

      // Save token
      await setAuthToken(response.data.access_token);

      // Navigate to Preferences
      navigation.reset({
        index: 0,
        routes: [{ name: 'Preferences' }],
      });
    } catch (error: any) {
      const { title, message } = formatErrorAlert(error);
      Alert.alert(title, message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text variant="headlineLarge" style={styles.title}>
          {mode === 'signup' ? 'Create Account' : 'Welcome Back'}
        </Text>

        <SegmentedButtons
          value={mode}
          onValueChange={(value) => setMode(value as 'login' | 'signup')}
          buttons={[
            { value: 'signup', label: 'Sign Up' },
            { value: 'login', label: 'Login' },
          ]}
          style={styles.segmentedButtons}
        />

        <TextInput
          label="Email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          mode="outlined"
          style={styles.input}
        />

        <TextInput
          label="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          mode="outlined"
          style={styles.input}
        />

        <Button
          mode="contained"
          onPress={handleAuth}
          loading={loading}
          disabled={loading}
          style={styles.button}
          contentStyle={styles.buttonContent}
        >
          {mode === 'signup' ? 'Sign Up' : 'Login'}
        </Button>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 40,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 32,
    textAlign: 'center',
  },
  segmentedButtons: {
    marginBottom: 32,
  },
  input: {
    marginBottom: 16,
  },
  button: {
    marginTop: 16,
    backgroundColor: '#8B5CF6',
  },
  buttonContent: {
    paddingVertical: 8,
  },
});
