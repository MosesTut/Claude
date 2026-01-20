// User Types
export interface User {
  id: string;
  email: string;
  display_name?: string;
  ai_disclosure_accepted: boolean;
  data_use_accepted: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Preference Types
export interface Preferences {
  id?: string;
  user_id?: string;
  start_date?: string;
  end_date?: string;
  trip_length_days?: number;
  interests?: string[];
  food_preferences?: string[];
  budget_level?: 'budget' | 'mid-range' | 'luxury';
  pace?: 'relaxed' | 'moderate' | 'packed';
  created_at?: string;
  updated_at?: string;
}

// City Types
export interface CityRecommendation {
  city_name: string;
  country: string;
  reasoning: string;
  match_score?: number;
}

// Itinerary Types
export interface DailyPlan {
  day: number;
  morning: {
    activity: string;
    location: string;
    duration: string;
    tips: string;
  };
  lunch: {
    restaurant: string;
    cuisine: string;
    price_range: string;
    neighborhood: string;
  };
  afternoon: {
    activity: string;
    location: string;
    duration: string;
    tips: string;
  };
  dinner: {
    restaurant: string;
    cuisine: string;
    price_range: string;
    neighborhood: string;
  };
  evening?: {
    activity: string;
    optional: boolean;
  };
}

export interface ItineraryData {
  city: string;
  country: string;
  trip_length_days: number;
  daily_plans: DailyPlan[];
  general_tips: string[];
}

export interface Itinerary {
  id: string;
  user_id: string;
  city_name: string;
  country: string;
  city_reasoning?: string;
  itinerary_data: ItineraryData;
  trip_length_days: number;
  ai_model: string;
  prompt_version: string;
  helpful_rating?: 'helpful' | 'not_helpful';
  created_at: string;
}

// Feedback Types
export type FeedbackType = 'inaccurate' | 'inappropriate' | 'missing_information' | 'other';

export interface Feedback {
  itinerary_id: string;
  feedback_type: FeedbackType;
  comments?: string;
}
