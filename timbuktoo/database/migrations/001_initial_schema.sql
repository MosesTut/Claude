-- Timbuktoo Initial Database Schema
-- PostgreSQL 14+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Cities table
CREATE TABLE cities (
    city_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    timezone TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    description TEXT,
    best_seasons TEXT[], -- ['spring', 'summer', 'fall', 'winter']
    currency TEXT,
    language TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(name, country)
);

-- Entity types: restaurant, bar, museum, nature, event, hotel, neighborhood
CREATE TABLE entities (
    entity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_id UUID NOT NULL REFERENCES cities(city_id) ON DELETE CASCADE,
    entity_type TEXT NOT NULL CHECK (
        entity_type IN ('restaurant', 'bar', 'museum', 'nature', 'event', 'hotel', 'neighborhood')
    ),
    name TEXT NOT NULL,
    description TEXT,
    price_tier TEXT CHECK (price_tier IN ('low', 'mid', 'high', 'luxury')),
    vibes TEXT[], -- ['luxury', 'local', 'nightlife', 'nature', 'historic']
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    phone TEXT,
    website TEXT,
    opening_hours JSONB,
    average_duration_minutes INTEGER,
    best_time_of_day TEXT[], -- ['morning', 'afternoon', 'evening', 'night']
    seasonality TEXT[], -- ['spring', 'summer', 'fall', 'winter']
    trust_tier INTEGER DEFAULT 1 CHECK (trust_tier BETWEEN 1 AND 5),
    source TEXT,
    last_verified DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_entities_city ON entities(city_id);
CREATE INDEX idx_entities_type ON entities(entity_type);
CREATE INDEX idx_entities_price ON entities(price_tier);

-- Vector embeddings (metadata only, actual vectors in ChromaDB)
CREATE TABLE vectors (
    vector_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(entity_id) ON DELETE CASCADE,
    vector_store_id TEXT NOT NULL, -- Reference to ChromaDB ID
    embedding_model TEXT DEFAULT 'sentence-transformers/all-MiniLM-L6-v2',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vectors_entity ON vectors(entity_id);
CREATE INDEX idx_vectors_store ON vectors(vector_store_id);

-- Trips
CREATE TABLE trips (
    trip_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID, -- Optional user tracking (anonymized)
    city_id UUID NOT NULL REFERENCES cities(city_id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INTEGER GENERATED ALWAYS AS (end_date - start_date + 1) STORED,
    preferences JSONB, -- User preferences (vibes, budget, etc.)
    itinerary JSONB, -- Full 7-day itinerary
    estimated_cost_usd DECIMAL(10, 2),
    weather_data JSONB,
    events_data JSONB,
    variant_id TEXT, -- For A/B testing
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trips_city ON trips(city_id);
CREATE INDEX idx_trips_dates ON trips(start_date, end_date);
CREATE INDEX idx_trips_variant ON trips(variant_id);

-- Feedback
CREATE TABLE feedback (
    feedback_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
    overall_rating INTEGER CHECK (overall_rating BETWEEN 1 AND 5),
    daily_ratings JSONB, -- {"day1": 5, "day2": 4, ...}
    comments TEXT,
    pacing_rating INTEGER CHECK (pacing_rating BETWEEN 1 AND 5),
    authenticity_rating INTEGER CHECK (authenticity_rating BETWEEN 1 AND 5),
    value_rating INTEGER CHECK (value_rating BETWEEN 1 AND 5),
    liked_entities UUID[], -- Array of entity_ids
    disliked_entities UUID[], -- Array of entity_ids
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feedback_trip ON feedback(trip_id);
CREATE INDEX idx_feedback_rating ON feedback(overall_rating);

-- Cost tracking
CREATE TABLE cost_tracking (
    cost_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID REFERENCES trips(trip_id) ON DELETE CASCADE,
    agent_type TEXT NOT NULL,
    model_used TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cost_usd DECIMAL(10, 6) NOT NULL,
    cached BOOLEAN DEFAULT false,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cost_trip ON cost_tracking(trip_id);
CREATE INDEX idx_cost_agent ON cost_tracking(agent_type);

-- Audit logs (SOC-2 compliance)
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type TEXT NOT NULL,
    user_id UUID,
    resource_type TEXT,
    resource_id UUID,
    action TEXT NOT NULL,
    ip_address INET,
    user_agent TEXT,
    status TEXT CHECK (status IN ('success', 'failure', 'error')),
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_event ON audit_logs(event_type);

-- Users (for RBAC)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'operator', 'viewer')),
    mfa_enabled BOOLEAN DEFAULT false,
    mfa_secret TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Update triggers
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_cities_modtime
    BEFORE UPDATE ON cities
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_entities_modtime
    BEFORE UPDATE ON entities
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_trips_modtime
    BEFORE UPDATE ON trips
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
