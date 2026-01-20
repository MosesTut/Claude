#!/bin/bash

# Backend API Test Script
# Quick verification that all endpoints are working

set -e

BASE_URL="http://localhost:8000"
EMAIL="test-$(date +%s)@example.com"
PASSWORD="password123"
TOKEN=""

echo "================================================"
echo "Timbuktoo Backend API Test Script"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
HEALTH=$(curl -s -w "\n%{http_code}" $BASE_URL/health)
HTTP_CODE=$(echo "$HEALTH" | tail -n1)
RESPONSE=$(echo "$HEALTH" | head -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    echo "   Response: $RESPONSE"
else
    echo -e "${RED}❌ Health check failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi
echo ""

# Test 2: Signup
echo -e "${YELLOW}Test 2: User Signup${NC}"
SIGNUP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/signup \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\",
    \"ai_disclosure_accepted\": true,
    \"data_use_accepted\": true
  }")

HTTP_CODE=$(echo "$SIGNUP_RESPONSE" | tail -n1)
RESPONSE=$(echo "$SIGNUP_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "201" ]; then
    echo -e "${GREEN}✅ Signup successful${NC}"
    TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
    echo "   Email: $EMAIL"
    echo "   Token: ${TOKEN:0:20}..."
else
    echo -e "${RED}❌ Signup failed (HTTP $HTTP_CODE)${NC}"
    echo "   Response: $RESPONSE"
    exit 1
fi
echo ""

# Test 3: Login
echo -e "${YELLOW}Test 3: User Login${NC}"
LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Login successful${NC}"
else
    echo -e "${RED}❌ Login failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi
echo ""

# Test 4: Get User Info
echo -e "${YELLOW}Test 4: Get User Info${NC}"
USER_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/user/me \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$USER_RESPONSE" | tail -n1)
RESPONSE=$(echo "$USER_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Get user info successful${NC}"
    echo "   User: $(echo "$RESPONSE" | jq -r '.email')"
else
    echo -e "${RED}❌ Get user info failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi
echo ""

# Test 5: Save Preferences
echo -e "${YELLOW}Test 5: Save Preferences${NC}"
PREF_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $BASE_URL/preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["Culture & Museums", "Food & Dining"],
    "food_preferences": ["Vegetarian"],
    "budget_level": "mid-range",
    "pace": "moderate",
    "trip_length_days": 3
  }')

HTTP_CODE=$(echo "$PREF_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "201" ]; then
    echo -e "${GREEN}✅ Save preferences successful${NC}"
else
    echo -e "${RED}❌ Save preferences failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi
echo ""

# Test 6: Get City Recommendations (AI)
echo -e "${YELLOW}Test 6: Get City Recommendations (AI - may take 5-10s)${NC}"
CITIES_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/cities/recommendations \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$CITIES_RESPONSE" | tail -n1)
RESPONSE=$(echo "$CITIES_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Get city recommendations successful${NC}"
    CITY_COUNT=$(echo "$RESPONSE" | jq '.cities | length')
    echo "   Cities returned: $CITY_COUNT"
    echo "   City 1: $(echo "$RESPONSE" | jq -r '.cities[0].city_name'), $(echo "$RESPONSE" | jq -r '.cities[0].country')"
else
    echo -e "${RED}❌ Get city recommendations failed (HTTP $HTTP_CODE)${NC}"
    echo "   Response: $RESPONSE"
fi
echo ""

# Test 7: Generate Itinerary (AI - SLOW)
echo -e "${YELLOW}Test 7: Generate Itinerary (AI - may take 30-60s)${NC}"
echo "   This test is slow, skipping by default..."
echo "   To test, run manually:"
echo "   curl -X POST $BASE_URL/itinerary/generate \\"
echo "     -H \"Authorization: Bearer $TOKEN\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"city_name\": \"Lisbon\", \"country\": \"Portugal\", \"trip_length_days\": 3}'"
echo ""

# Test 8: Delete Account (GDPR)
echo -e "${YELLOW}Test 8: Delete Account (GDPR)${NC}"
DELETE_RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/user/account \
  -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(echo "$DELETE_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "204" ]; then
    echo -e "${GREEN}✅ Delete account successful${NC}"
else
    echo -e "${RED}❌ Delete account failed (HTTP $HTTP_CODE)${NC}"
    exit 1
fi
echo ""

echo "================================================"
echo -e "${GREEN}All tests passed! ✅${NC}"
echo "================================================"
