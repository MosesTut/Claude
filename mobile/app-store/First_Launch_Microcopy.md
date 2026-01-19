# First-Launch UX Microcopy - Timbuktoo Mobile

**Last Updated**: 2024-07-16
**Purpose**: Approval-critical UI copy for all first-launch screens
**Status**: Production-Ready

This document provides exact, copy-pasteable microcopy for all first-launch screens, optimized for App Store approval and user onboarding conversion.

---

## Onboarding Flow Overview

**Flow**: Splash → Welcome → AI Disclosure → Data Use → Authentication → Preferences → City Recommendation → Itinerary

**Critical Screens**:
1. **Welcome** - Brand introduction, value proposition
2. **AI Disclosure** (MANDATORY) - AI transparency, consent checkbox
3. **Data Use** - Privacy and data usage explanation
4. **Permissions** - Notifications (optional)

**Conversion Goals**:
- Complete onboarding: 80%+ (industry benchmark: 60-70%)
- Accept AI disclosure: 100% required (blocking)
- Enable notifications: 40%+ (optional)

---

## Screen 1: Welcome

### Title
```
Welcome to Timbuktoo
```

### Body
```
Your AI-powered travel concierge for personalized trip planning.
```

### Supporting Copy (Optional)
```
Plan smarter trips in minutes. Get day-by-day itineraries tailored to your
interests, food preferences, and budget.
```

### Call-to-Action (CTA)
```
Get Started
```

### Design Notes
- **Title**: 28-32pt, Bold, Dark gray or black
- **Body**: 16-18pt, Regular, Medium gray
- **CTA Button**: Primary brand color (blue/teal), 16-18pt Semibold
- **Background**: White or light gradient
- **Illustration**: Travel-themed graphic (airplane, map, suitcase) - optional but recommended
- **Progress Indicator**: 1/4 dots (bottom center) - shows user they're at step 1 of 4

### Alternative Copy (A/B Test)

**Variant A - Benefit-Focused**:
```
Title: Plan Your Best Trip Yet
Body: AI-powered itineraries tailored to your style, budget, and interests.
CTA: Start Planning
```

**Variant B - Time-Saving**:
```
Title: Skip the Research
Body: Get personalized travel plans in minutes, not hours.
CTA: Get Started
```

**Variant C - Trust-Building**:
```
Title: Welcome to Timbuktoo
Body: Trusted by 10,000+ travelers for personalized trip planning.
CTA: See How It Works
```

---

## Screen 2: AI Disclosure (MANDATORY - CRITICAL FOR APP STORE APPROVAL)

### Title
```
About AI Recommendations
```

### Body
```
Timbuktoo uses artificial intelligence to generate travel suggestions.

AI-generated content may be inaccurate or incomplete. Verify critical details
before booking.
```

### Warning Section (Yellow Box or Highlighted)
```
Important:
• AI recommendations are informational only
• Verify prices, hours, and availability
• Report any issues using our feedback tools
```

### Consent Checkbox (REQUIRED)
```
☐ I understand that itineraries are AI-generated
```

### Call-to-Action (CTA)
```
I Understand
```
**Button State**: Disabled (grayed out) until checkbox is checked

### Design Notes
- **Title**: 24-28pt, Bold, Dark gray or black
- **Body**: 16pt, Regular, Dark gray (#424242)
- **Warning Section**: Yellow background (#FFF9C4), orange icon ⚠️
- **Checkbox**: Material Design checkbox (unchecked by default)
- **Checkbox Label**: 14-16pt, Medium gray, clear and readable
- **CTA Button**: Disabled state (gray) until checkbox checked, then primary color
- **Progress Indicator**: 2/4 dots
- **Blocking Behavior**: User CANNOT tap "I Understand" until checkbox is checked

**CRITICAL**: This screen is MANDATORY for Apple App Store approval. Without this, app will be rejected under Guideline 5.1.1 (AI Disclosure).

### Alternative Copy (Simpler Language)

**Variant A - Plain Language**:
```
Title: AI Transparency
Body: We use AI to suggest travel plans. These suggestions may not be perfect.
Always double-check before you book.

Checkbox: ☐ I understand itineraries are created by AI
```

**Variant B - Trust-Building**:
```
Title: How Timbuktoo Works
Body: Our AI analyzes your preferences to recommend destinations and create
itineraries. While we strive for accuracy, AI-generated content may contain
errors. Please verify important details.

Checkbox: ☐ I understand and accept that recommendations are AI-generated
```

---

## Screen 3: Data Use

### Title
```
Your Privacy Matters
```

### Body
```
We collect your travel preferences to personalize recommendations. Your data is
never sold or shared.
```

### Data Collection Breakdown
```
What We Collect:
• Email address (for your account)
• Travel preferences (to personalize trips)
• Usage data (to improve the app)

What We Don't Collect:
• Location data (GPS)
• Contacts or photos
• Payment info (handled by Apple/Google)
```

### Links
```
[Privacy Policy] | [Terms of Service]
```

### Call-to-Action (CTA)
```
Continue
```

### Design Notes
- **Title**: 24-28pt, Bold
- **Body**: 16pt, Regular
- **Breakdown**: Bulleted list, 14pt, Regular
- **Icons**: ✓ for "What We Collect", ❌ for "What We Don't Collect"
- **Links**: 14pt, Underlined, Brand color (blue/teal)
- **CTA Button**: Primary brand color
- **Progress Indicator**: 3/4 dots

### Alternative Copy (Shorter)

**Variant A - Concise**:
```
Title: Privacy First
Body: Your preferences are used to personalize trips. We never sell your data.
CTA: Got It
```

**Variant B - Benefit-Focused**:
```
Title: Personalized Just for You
Body: We use your travel preferences to create perfect itineraries. Your data
stays private and secure.
CTA: Continue
```

---

## Screen 4: Permissions (Optional)

### Title
```
Stay Updated
```

### Body
```
Enable notifications for itinerary updates and reminders.
```

### Icon
```
🔔 (Bell icon, large, centered)
```

### Call-to-Action (CTA)
```
Allow Notifications
```

### Secondary CTA
```
Skip for Now
```

### Design Notes
- **Title**: 24-28pt, Bold
- **Body**: 16pt, Regular
- **Icon**: 64x64pt or larger, centered above body text
- **Primary CTA**: Primary brand color (blue/teal)
- **Secondary CTA**: Text button (no fill), gray color
- **Progress Indicator**: 4/4 dots (last screen)
- **Blocking Behavior**: NOT required, user can skip

**Alternative Copy (Value-Focused)**:

**Variant A - Reminder-Focused**:
```
Title: Never Miss a Detail
Body: Get reminders for restaurant reservations, activities, and travel tips.
CTA: Enable Reminders
```

**Variant B - Benefit-Heavy**:
```
Title: Notifications That Help
Body: We'll only send helpful reminders—no spam, no ads, just your trip details.
CTA: Turn On Notifications
```

---

## Screen 5: Preferences (Post-Onboarding)

### Title
```
Tell Us What You Love
```

### Body
```
Build your first trip by sharing your travel style.
```

### Section 1: Interests
```
What interests you? (Select all that apply)
□ Culture & History
□ Food & Dining
□ Nature & Outdoors
□ Adventure & Sports
□ Nightlife & Entertainment
□ Relaxation & Wellness
□ Shopping & Markets
□ Art & Museums
```

### Section 2: Food Preferences
```
Food Preferences
◉ Adventurous Eater (Try everything!)
○ Vegetarian
○ Vegan
○ Dietary Restrictions
```

### Section 3: Budget
```
Budget
[Slider: Low ——●—— Medium ——— High ——— Luxury]
```

### Section 4: Dates (Optional)
```
Travel Dates (Optional)
[Date Picker: Start Date] → [Date Picker: End Date]
```

### Call-to-Action (CTA)
```
Build My First Trip
```

### Design Notes
- **Title**: 24-28pt, Bold
- **Body**: 16pt, Regular
- **Section Headers**: 18pt, Semibold
- **Checkboxes**: Material Design checkboxes (multi-select)
- **Radio Buttons**: Material Design radio buttons (single-select)
- **Slider**: Material Design slider with labels
- **Date Picker**: Native iOS/Android date picker
- **CTA Button**: Primary brand color, bottom of screen (sticky footer)

### Alternative Copy (Shorter)

**Variant A - Question Format**:
```
Title: What Kind of Traveler Are You?
Body: Help us personalize your trip.
CTA: Get Recommendations
```

**Variant B - Excitement-Building**:
```
Title: Let's Plan Your Perfect Trip
Body: Select your interests and we'll do the rest.
CTA: Show Me Destinations
```

---

## Additional Microcopy Elements

### Loading States

**Generating City Recommendations** (5-10 seconds):
```
Finding your perfect destinations...
```

**Generating Itinerary** (30-60 seconds):
```
Creating your personalized itinerary...

This may take 30-60 seconds. We're analyzing hundreds of options to find the
best restaurants, attractions, and experiences for you.
```

**Alternative Loading Copy**:
```
✈️ Searching destinations...
🍽️ Finding top restaurants...
🎨 Curating activities...
✅ Building your itinerary...
```

### Error States

**Network Error**:
```
Title: Connection Lost
Body: Please check your internet connection and try again.
CTA: Retry
```

**API Error** (500 Internal Server Error):
```
Title: Something Went Wrong
Body: We're having trouble generating your itinerary. Please try again in a
few moments.
CTA: Try Again
```

**Rate Limit Error** (Free Tier):
```
Title: Monthly Limit Reached
Body: You've used 3 of 3 free itineraries this month. Upgrade to Pro for
unlimited planning.
CTA: Upgrade to Pro
Secondary CTA: Wait Until [Date]
```

**Authentication Error** (Invalid JWT):
```
Title: Session Expired
Body: Please log in again to continue.
CTA: Log In
```

### Success States

**Account Created**:
```
Title: Welcome to Timbuktoo!
Body: Your account has been created. Let's plan your first trip.
CTA: Get Started
```

**Itinerary Generated**:
```
Title: Your Itinerary is Ready!
Body: We've created a personalized [X]-day plan for [City Name].
CTA: View Itinerary
```

**Feedback Submitted**:
```
Title: Thank You!
Body: Your feedback helps us improve recommendations for everyone.
CTA: Close
```

**Account Deleted**:
```
Title: Account Deleted
Body: Your account and all data have been permanently deleted. We're sorry to
see you go.
CTA: OK
```

### Empty States

**No Itineraries Yet**:
```
Title: No Trips Yet
Body: Generate your first personalized itinerary to get started.
CTA: Plan a Trip
```

**No Saved Trips**:
```
Title: No Saved Trips
Body: Save your favorite itineraries to access them anytime.
CTA: Explore Destinations
```

---

## Microcopy Guidelines

### Tone & Voice

**Brand Voice**: Friendly, helpful, trustworthy
- ✅ Do: "We're here to help you plan amazing trips"
- ❌ Don't: "Timbuktoo is the best travel app ever" (too salesy)

**Clarity Over Cleverness**:
- ✅ Do: "Generate your personalized itinerary"
- ❌ Don't: "Let the AI magic begin!" (too vague)

**Respectful of User Time**:
- ✅ Do: "This may take 30-60 seconds"
- ❌ Don't: "Hang tight!" (doesn't set expectations)

### Character Limits

**Buttons**: 20 characters max (ideally 10-15)
- ✅ "Get Started" (11 chars)
- ❌ "Click Here to Get Started with Your First Trip" (48 chars, too long)

**Headlines**: 40 characters max (mobile screens)
- ✅ "Welcome to Timbuktoo" (20 chars)
- ❌ "Welcome to Timbuktoo - Your AI-Powered Travel Concierge" (57 chars, truncated on mobile)

**Body Text**: 160 characters max per paragraph (mobile readability)
- ✅ "Your AI-powered travel concierge for personalized trip planning." (64 chars)
- ❌ Long paragraphs that require scrolling (user drop-off)

### Accessibility

**Screen Reader-Friendly**:
- Use descriptive button labels: "Get Started" (not "Click Here")
- Provide alt text for icons: "Notification bell icon"
- Use semantic HTML/native components (auto-labeled)

**Dyslexia-Friendly**:
- Short sentences (10-15 words max)
- Clear paragraph breaks
- Avoid all caps (harder to read)

**Non-Native English Speakers**:
- Simple vocabulary (avoid idioms like "let's get the ball rolling")
- Clear, direct language

---

## Localization (Optional - Phase 2)

### Spanish (es-ES)

**Welcome**:
```
Bienvenido a Timbuktoo
Tu asistente de viajes con IA para planificación personalizada.
Comenzar
```

**AI Disclosure**:
```
Acerca de las Recomendaciones de IA
Timbuktoo usa inteligencia artificial para generar sugerencias de viaje.
El contenido generado por IA puede ser inexacto o incompleto.

☐ Entiendo que los itinerarios son generados por IA
Entiendo
```

**Data Use**:
```
Tu Privacidad Importa
Recopilamos tus preferencias de viaje para personalizar recomendaciones.
Tus datos nunca se venden ni comparten.
Continuar
```

**Preferences**:
```
Cuéntanos Qué Te Gusta
Construye tu primer viaje compartiendo tu estilo de viajar.
Construir Mi Primer Viaje
```

### French (fr-FR)

**Welcome**:
```
Bienvenue sur Timbuktoo
Votre concierge de voyage IA pour une planification personnalisée.
Commencer
```

**AI Disclosure**:
```
À Propos des Recommandations IA
Timbuktoo utilise l'intelligence artificielle pour générer des suggestions de
voyage. Le contenu généré par IA peut être inexact ou incomplet.

☐ Je comprends que les itinéraires sont générés par IA
Je Comprends
```

---

## App Store Review Compliance Checklist

**Before Submitting**:

- [ ] AI disclosure screen (Screen 2) is MANDATORY and blocking
- [ ] Consent checkbox must be checked to proceed
- [ ] Privacy Policy and Terms of Service links functional
- [ ] Loading states set clear expectations (30-60 seconds for itinerary)
- [ ] Error states provide actionable solutions (Retry, Contact Support)
- [ ] No misleading language ("free" when it's a trial)
- [ ] No pressure tactics ("Only 3 spots left!", "Limited time!")
- [ ] Permissions (notifications) are optional, not required
- [ ] All copy reviewed by legal team
- [ ] All copy tested on devices (not truncated)

---

**Last Updated**: 2024-07-16
**Next Review**: After first user feedback (post-launch)
**Owner**: Product + Content teams
