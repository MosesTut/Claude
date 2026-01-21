/**
 * Form validation utilities
 * Provides reusable validation functions for all forms
 */

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

// Email validation
export function validateEmail(email: string): ValidationResult {
  if (!email) {
    return { isValid: false, error: 'Email is required' };
  }

  if (email.length < 3) {
    return { isValid: false, error: 'Email is too short' };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { isValid: false, error: 'Please enter a valid email address' };
  }

  return { isValid: true };
}

// Password validation (strong password)
export function validatePassword(password: string, requireStrong: boolean = true): ValidationResult {
  if (!password) {
    return { isValid: false, error: 'Password is required' };
  }

  if (password.length < 8) {
    return { isValid: false, error: 'Password must be at least 8 characters' };
  }

  if (requireStrong) {
    if (!/[A-Z]/.test(password)) {
      return { isValid: false, error: 'Password must contain at least one uppercase letter' };
    }

    if (!/[a-z]/.test(password)) {
      return { isValid: false, error: 'Password must contain at least one lowercase letter' };
    }

    if (!/[0-9]/.test(password)) {
      return { isValid: false, error: 'Password must contain at least one number' };
    }
  }

  return { isValid: true };
}

// Password confirmation
export function validatePasswordMatch(password: string, confirmPassword: string): ValidationResult {
  if (!confirmPassword) {
    return { isValid: false, error: 'Please confirm your password' };
  }

  if (password !== confirmPassword) {
    return { isValid: false, error: 'Passwords do not match' };
  }

  return { isValid: true };
}

// Trip length validation
export function validateTripLength(tripLength: string): ValidationResult {
  if (!tripLength) {
    return { isValid: false, error: 'Trip length is required' };
  }

  const num = parseInt(tripLength, 10);

  if (isNaN(num)) {
    return { isValid: false, error: 'Please enter a valid number' };
  }

  if (num < 1) {
    return { isValid: false, error: 'Trip must be at least 1 day' };
  }

  if (num > 30) {
    return { isValid: false, error: 'Trip cannot exceed 30 days (try breaking it into multiple trips!)' };
  }

  return { isValid: true };
}

// Interests validation
export function validateInterests(interests: string[]): ValidationResult {
  if (!interests || interests.length === 0) {
    return { isValid: false, error: 'Please select at least one interest' };
  }

  if (interests.length > 8) {
    return { isValid: false, error: 'Please select no more than 8 interests' };
  }

  return { isValid: true };
}

// Food preferences validation (optional)
export function validateFoodPreferences(foodPreferences: string[]): ValidationResult {
  // Food preferences are optional, so empty array is valid
  if (!foodPreferences || foodPreferences.length === 0) {
    return { isValid: true };
  }

  if (foodPreferences.length > 5) {
    return { isValid: false, error: 'Please select no more than 5 food preferences' };
  }

  return { isValid: true };
}

// Comments validation (for feedback)
export function validateComments(comments: string, maxLength: number = 500): ValidationResult {
  // Comments are optional
  if (!comments) {
    return { isValid: true };
  }

  if (comments.length > maxLength) {
    return {
      isValid: false,
      error: `Comments must be less than ${maxLength} characters (${comments.length}/${maxLength})`,
    };
  }

  return { isValid: true };
}

// City name validation
export function validateCityName(cityName: string): ValidationResult {
  if (!cityName || cityName.trim().length === 0) {
    return { isValid: false, error: 'Please select a city' };
  }

  return { isValid: true };
}

// Generic required field
export function validateRequired(value: any, fieldName: string): ValidationResult {
  if (!value || (typeof value === 'string' && value.trim().length === 0)) {
    return { isValid: false, error: `${fieldName} is required` };
  }

  return { isValid: true };
}

// Validate entire preferences form
export interface PreferencesForm {
  interests: string[];
  foodPreferences: string[];
  budgetLevel: string;
  pace: string;
  tripLength: string;
}

export function validatePreferencesForm(form: PreferencesForm): ValidationResult {
  // Validate interests
  const interestsResult = validateInterests(form.interests);
  if (!interestsResult.isValid) {
    return interestsResult;
  }

  // Validate food preferences (optional)
  const foodResult = validateFoodPreferences(form.foodPreferences);
  if (!foodResult.isValid) {
    return foodResult;
  }

  // Validate trip length
  const tripLengthResult = validateTripLength(form.tripLength);
  if (!tripLengthResult.isValid) {
    return tripLengthResult;
  }

  // Budget and pace are always valid (have defaults)
  return { isValid: true };
}

// Validate signup form
export interface SignupForm {
  email: string;
  password: string;
  confirmPassword: string;
}

export function validateSignupForm(form: SignupForm): ValidationResult {
  // Validate email
  const emailResult = validateEmail(form.email);
  if (!emailResult.isValid) {
    return emailResult;
  }

  // Validate password
  const passwordResult = validatePassword(form.password);
  if (!passwordResult.isValid) {
    return passwordResult;
  }

  // Validate password match
  const matchResult = validatePasswordMatch(form.password, form.confirmPassword);
  if (!matchResult.isValid) {
    return matchResult;
  }

  return { isValid: true };
}

// Validate login form
export interface LoginForm {
  email: string;
  password: string;
}

export function validateLoginForm(form: LoginForm): ValidationResult {
  // Validate email
  const emailResult = validateEmail(form.email);
  if (!emailResult.isValid) {
    return emailResult;
  }

  // Validate password (less strict for login)
  const passwordResult = validatePassword(form.password, false);
  if (!passwordResult.isValid) {
    return passwordResult;
  }

  return { isValid: true };
}

// Helper: Check if string is empty or whitespace
export function isEmpty(value: string): boolean {
  return !value || value.trim().length === 0;
}

// Helper: Sanitize input (remove dangerous characters)
export function sanitizeInput(input: string): string {
  return input.trim().replace(/[<>]/g, '');
}

// Helper: Format error message for display
export function formatValidationError(error: string): string {
  return error.charAt(0).toUpperCase() + error.slice(1);
}
