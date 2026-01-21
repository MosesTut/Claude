import { AxiosError } from 'axios';

// Error types
export enum ErrorType {
  NETWORK = 'network',
  AUTH = 'auth',
  VALIDATION = 'validation',
  RATE_LIMIT = 'rate_limit',
  SERVER = 'server',
  UNKNOWN = 'unknown',
}

export interface AppError {
  type: ErrorType;
  title: string;
  message: string;
  action?: string;
  code?: string;
}

// User-friendly error messages
const ERROR_MESSAGES: Record<string, AppError> = {
  // Network errors
  NETWORK_ERROR: {
    type: ErrorType.NETWORK,
    title: 'Connection Problem',
    message: 'Unable to connect to the server. Please check your internet connection and try again.',
    action: 'Retry',
  },
  TIMEOUT: {
    type: ErrorType.NETWORK,
    title: 'Request Timeout',
    message: 'The request took too long. This might be due to slow internet or high server load.',
    action: 'Try Again',
  },

  // Auth errors
  UNAUTHORIZED: {
    type: ErrorType.AUTH,
    title: 'Session Expired',
    message: 'Your session has expired. Please log in again.',
    action: 'Log In',
  },
  INVALID_CREDENTIALS: {
    type: ErrorType.AUTH,
    title: 'Invalid Credentials',
    message: 'The email or password you entered is incorrect. Please try again.',
    action: 'Retry',
  },
  USER_EXISTS: {
    type: ErrorType.VALIDATION,
    title: 'Account Already Exists',
    message: 'An account with this email already exists. Please log in instead.',
    action: 'Log In',
  },

  // Rate limiting
  RATE_LIMIT_FREE: {
    type: ErrorType.RATE_LIMIT,
    title: 'Free Tier Limit Reached',
    message: "You've reached your limit of 3 itineraries this month. Upgrade to Pro for unlimited itineraries.",
    action: 'Upgrade to Pro',
  },
  RATE_LIMIT_GENERIC: {
    type: ErrorType.RATE_LIMIT,
    title: 'Too Many Requests',
    message: 'You are making requests too quickly. Please wait a moment and try again.',
    action: 'Wait',
  },

  // AI/Generation errors
  AI_GENERATION_FAILED: {
    type: ErrorType.SERVER,
    title: 'Generation Failed',
    message: 'We encountered an issue generating your itinerary. Our AI service might be temporarily unavailable.',
    action: 'Try Again',
  },
  NO_CITIES_FOUND: {
    type: ErrorType.VALIDATION,
    title: 'No Matches Found',
    message: 'We couldn\'t find cities matching your preferences. Try adjusting your criteria.',
    action: 'Change Preferences',
  },

  // Validation errors
  INVALID_INPUT: {
    type: ErrorType.VALIDATION,
    title: 'Invalid Input',
    message: 'Please check your input and try again.',
    action: 'Fix',
  },
  MISSING_PREFERENCES: {
    type: ErrorType.VALIDATION,
    title: 'Preferences Required',
    message: 'Please select your travel preferences before continuing.',
    action: 'Go Back',
  },

  // Server errors
  SERVER_ERROR: {
    type: ErrorType.SERVER,
    title: 'Server Error',
    message: 'Something went wrong on our end. Our team has been notified and is working on it.',
    action: 'Try Again Later',
  },
  MAINTENANCE: {
    type: ErrorType.SERVER,
    title: 'Maintenance Mode',
    message: 'Timbuktoo is currently undergoing maintenance. We\'ll be back shortly!',
    action: 'Check Status',
  },
};

/**
 * Parse API error and return user-friendly error object
 */
export function parseApiError(error: any): AppError {
  // Network error (no response)
  if (!error.response) {
    if (error.code === 'ECONNABORTED') {
      return ERROR_MESSAGES.TIMEOUT;
    }
    return ERROR_MESSAGES.NETWORK_ERROR;
  }

  const status = error.response.status;
  const data = error.response.data;
  const detail = data?.detail || '';

  // Handle specific error codes
  switch (status) {
    case 401:
      return ERROR_MESSAGES.UNAUTHORIZED;

    case 403:
      // Check if it's rate limiting
      if (detail.includes('limit') || detail.includes('itineraries')) {
        return ERROR_MESSAGES.RATE_LIMIT_FREE;
      }
      return {
        type: ErrorType.AUTH,
        title: 'Access Denied',
        message: detail || 'You do not have permission to perform this action.',
        action: 'Go Back',
      };

    case 409:
      // Conflict - likely user already exists
      if (detail.includes('email') || detail.includes('exists')) {
        return ERROR_MESSAGES.USER_EXISTS;
      }
      return {
        type: ErrorType.VALIDATION,
        title: 'Conflict',
        message: detail,
        action: 'Retry',
      };

    case 422:
      // Validation error
      return {
        type: ErrorType.VALIDATION,
        title: 'Validation Error',
        message: detail || 'Please check your input and try again.',
        action: 'Fix',
      };

    case 429:
      return ERROR_MESSAGES.RATE_LIMIT_GENERIC;

    case 500:
    case 502:
    case 503:
      if (detail.includes('AI') || detail.includes('Claude')) {
        return ERROR_MESSAGES.AI_GENERATION_FAILED;
      }
      return ERROR_MESSAGES.SERVER_ERROR;

    case 504:
      return ERROR_MESSAGES.TIMEOUT;

    default:
      // Return custom message from server if available
      if (detail) {
        return {
          type: ErrorType.UNKNOWN,
          title: 'Error',
          message: detail,
          action: 'Try Again',
        };
      }
      return ERROR_MESSAGES.SERVER_ERROR;
  }
}

/**
 * Get error message for specific validation
 */
export function getValidationError(field: string, value: any): string | null {
  switch (field) {
    case 'email':
      if (!value) return 'Email is required';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        return 'Please enter a valid email address';
      }
      return null;

    case 'password':
      if (!value) return 'Password is required';
      if (value.length < 8) return 'Password must be at least 8 characters';
      if (!/[A-Z]/.test(value)) return 'Password must contain at least one uppercase letter';
      if (!/[a-z]/.test(value)) return 'Password must contain at least one lowercase letter';
      if (!/[0-9]/.test(value)) return 'Password must contain at least one number';
      return null;

    case 'tripLength':
      const num = parseInt(value);
      if (isNaN(num)) return 'Please enter a valid number';
      if (num < 1) return 'Trip must be at least 1 day';
      if (num > 30) return 'Trip cannot exceed 30 days';
      return null;

    case 'interests':
      if (!value || value.length === 0) {
        return 'Please select at least one interest';
      }
      return null;

    default:
      return null;
  }
}

/**
 * Format error for display in Alert
 */
export function formatErrorAlert(error: any): { title: string; message: string } {
  const appError = parseApiError(error);
  return {
    title: appError.title,
    message: appError.message,
  };
}
