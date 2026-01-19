# Privacy Policy - Mobile App Addendum

**Effective Date**: 2024-07-16
**Last Updated**: 2024-07-16
**Applies To**: Timbuktoo Mobile App (iOS & Android)

This Mobile App Addendum supplements our main Privacy Policy (available at https://timbuktoo.ai/privacy) with mobile-specific practices.

---

## 1. AI Usage (Apple App Store Requirement)

**AI Transparency**:

"This app uses artificial intelligence to generate travel recommendations. AI-generated content may be inaccurate or incomplete."

**What This Means**:
- Timbuktoo uses Anthropic's Claude API to generate personalized travel itineraries
- AI-generated recommendations are informational only
- Users are advised to independently verify all recommendations before making travel decisions
- Timbuktoo does not guarantee accuracy, pricing, availability, or safety of any recommendation

**User Consent**:
- During onboarding, users must explicitly consent to AI-generated content
- Consent checkbox: "I understand itineraries are AI-generated"
- Users cannot proceed without giving consent

---

## 2. Data Collection (Mobile-Specific)

**Data We Collect**:

| Data Type | Purpose | Linked to User | Used for Tracking |
|-----------|---------|----------------|-------------------|
| **Email Address** | Account creation, authentication | Yes | No |
| **Travel Preferences** | Personalization (interests, food, budget, dates) | Yes | No |
| **User-Generated Content** | Feedback, comments, issue reports | Yes | No |
| **AI-Generated Content** | Itineraries created by AI for the user | Yes | No |
| **Usage Data** | App analytics (screen views, button clicks) | No | No |
| **Device Information** | Platform (iOS/Android), OS version, app version | No | No |

**What We DO NOT Collect**:
- ❌ Location data (GPS coordinates)
- ❌ Contacts
- ❌ Photos
- ❌ Microphone/camera access
- ❌ Payment information (handled by Stripe, not stored by Timbuktoo)

---

## 3. How We Use Your Data

**Purposes**:

1. **Service Delivery**:
   - Generate personalized AI itineraries
   - Authenticate users (JWT tokens)
   - Store preferences for future trips

2. **App Improvement**:
   - Aggregate analytics (e.g., "50% of users select 'Food & Dining' interest")
   - A/B testing (e.g., comparing itinerary variants)
   - Bug tracking and performance monitoring

3. **Compliance**:
   - Store feedback and issue reports (required for App Store approval)
   - Audit logs for security incidents

**Legal Basis** (GDPR):
- **Legitimate Interest**: Service delivery, app improvement
- **Consent**: Marketing emails (opt-in only, not required for app use)

---

## 4. Data Sharing

**Third Parties We Share With**:

| Third Party | Data Shared | Purpose | Data Protection |
|-------------|-------------|---------|-----------------|
| **Anthropic** | Travel preferences (NOT email or PII) | AI itinerary generation | DPA signed, SOC-2 certified |
| **AWS** | All data (encrypted) | Infrastructure hosting (RDS, S3) | DPA signed, SOC-2 certified |
| **Datadog** | Usage logs (PII masked) | Monitoring, error tracking | DPA signed, SOC-2 certified |
| **Stripe** | Payment info (NOT stored by Timbuktoo) | Payment processing | PCI DSS certified |

**What We DO NOT Do**:
- ❌ Sell your data to third parties
- ❌ Share PII with advertisers
- ❌ Use your data to train AI models (Anthropic does not train on customer data per their DPA)

---

## 5. Data Security

**Encryption**:
- **In Transit**: TLS 1.2+ (HTTPS for all API calls)
- **At Rest**: AES-256 (AWS RDS, S3)
- **On Device**: Secure storage (Keychain on iOS, Keystore on Android)

**Authentication**:
- JWT tokens (30-day expiration)
- Stored in secure storage (not accessible by other apps)
- Tokens deleted on logout or account deletion

**Access Controls**:
- Role-based access control (RBAC) on backend
- Multi-factor authentication (MFA) for Timbuktoo employees
- Quarterly access reviews

---

## 6. Data Retention

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| **Account Data** | Until account deletion | Immediate deletion upon user request |
| **Travel Preferences** | Until account deletion | Immediate deletion upon user request |
| **Itineraries** | 2 years after last login | Automated deletion (PostgreSQL job) |
| **Feedback** | 5 years | Automated deletion (compliance requirement) |
| **Usage Logs** | 90 days | Automated deletion (Datadog) |

**Account Deletion**:
- Users can delete their account from Settings → Delete My Data
- Deletion request processed within 30 days (GDPR/CCPA requirement)
- Confirmation email sent upon completion

---

## 7. User Rights

**Your Rights** (GDPR & CCPA):

| Right | How to Exercise |
|-------|-----------------|
| **Right to Access** | Email dpo@timbuktoo.ai (30-day response SLA) |
| **Right to Rectification** | Update in app Settings or email support@timbuktoo.ai |
| **Right to Erasure** | Settings → Delete My Data or email dpo@timbuktoo.ai |
| **Right to Portability** | Email dpo@timbuktoo.ai for JSON export |
| **Right to Object** | Email dpo@timbuktoo.ai to opt-out of analytics |

---

## 8. Children's Privacy

Timbuktoo is **not intended for children under 13** (or 16 in EEA).

If we learn we have collected data from a child without parental consent, we will delete it immediately.

---

## 9. International Data Transfers

**Data Location**:
- Primary: AWS us-east-1 (Virginia, USA)
- Backup: AWS us-west-2 (Oregon, USA)

**EU Customers**:
- Standard Contractual Clauses (SCCs) in place with AWS
- GDPR-compliant data transfers
- Right to object to international transfers (email dpo@timbuktoo.ai)

---

## 10. Changes to This Policy

We will notify you of material changes via:
- In-app notification
- Email (if you have an account)
- Updated "Last Updated" date at top of this policy

Continued use of the app after changes constitutes acceptance.

---

## 11. Contact Us

**Data Protection Officer (DPO)**: dpo@timbuktoo.ai

**General Privacy Questions**: privacy@timbuktoo.ai

**Support**: support@timbuktoo.ai

**Mailing Address**:
Timbuktoo Inc.
[Address]
San Francisco, CA 94102
United States

---

## 12. App Store Privacy Nutrition Label (iOS)

**For Apple App Store submissions**, declare the following:

**Data Collected**:
- Email Address (Linked to User, Account Functionality)
- Travel Preferences (Linked to User, Personalization)
- User Content (AI-Generated Itineraries, Linked to User)
- Product Interaction (Not Linked to User, Analytics)

**Data Not Collected**:
- Location
- Contacts
- Photos
- Microphone/Camera
- Payment Info (handled by Stripe)

**Data Practices**:
- ✅ Data encrypted in transit
- ✅ Data encrypted at rest
- ✅ User can request data deletion
- ❌ Data NOT used for tracking

---

## 13. Google Play Data Safety (Android)

**For Google Play submissions**, declare the following:

**Data Collection**:
- Account info (Email)
- App activity (In-app interactions)
- App info and performance (Crash logs)

**Data Sharing**:
- Data shared with service providers (Anthropic, AWS, Datadog)
- No data sold to third parties

**Security Practices**:
- Data encrypted in transit (TLS 1.2+)
- Data encrypted at rest (AES-256)
- User-initiated data deletion
- Independent security review (annual penetration testing)

---

## Appendix: AI Content Moderation

**How We Monitor AI-Generated Content**:

1. **User Feedback**:
   - Users can report inaccurate or inappropriate recommendations
   - All reports reviewed by compliance team within 48 hours

2. **Automated Checks**:
   - Source attribution required (OSM, Wikidata, TripAdvisor)
   - Trust tier filtering (≥70% tier 4-5 sources)
   - Hallucination detection (cross-check with vector database)

3. **Human Review**:
   - 5% sample rate for high-cost trips (> $0.60 AI cost)
   - 100% review of reported content

4. **Actions Taken**:
   - Inaccurate content: Remove from knowledge base, retrain filters
   - Inappropriate content: Immediate removal, alert compliance team
   - Repeated issues: Improve AI prompts, update safety rules

**Transparency**:
- Quarterly AI safety reports published (aggregate data only, no user PII)
- User feedback incorporated into product improvements

---

**This Mobile App Addendum is incorporated into the main Privacy Policy and has the same legal effect.**

**Last Updated**: 2024-07-16
**Version**: 1.0
