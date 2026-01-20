// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000',
  TIMEOUT: 60000, // 60 seconds for AI generation
};

export const ENDPOINTS = {
  // Auth
  SIGNUP: '/auth/signup',
  LOGIN: '/auth/login',

  // User
  GET_USER: '/user/me',
  DELETE_ACCOUNT: '/user/account',

  // Preferences
  SAVE_PREFERENCES: '/preferences',
  GET_PREFERENCES: '/preferences',

  // Cities
  GET_CITY_RECOMMENDATIONS: '/cities/recommendations',

  // Itineraries
  GENERATE_ITINERARY: '/itinerary/generate',
  GET_ITINERARIES: '/itinerary',
  GET_ITINERARY_BY_ID: (id: string) => `/itinerary/${id}`,
  RATE_ITINERARY: (id: string) => `/itinerary/${id}/rating`,

  // Feedback
  SUBMIT_FEEDBACK: '/feedback',
};
