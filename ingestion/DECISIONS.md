# Design Decisions

## 1. SAP Data — Flat File CSV Export
**Decision:** Accept SAP data as a flat CSV export rather than IDoc or OData API.

**Reason:** Most mid-market SAP customers export procurement data via transaction MB51 or ME2M as CSV. IDoc requires direct system access and enterprise integration which is outside the scope of an ingestion service. CSV is the most common self-service export format used by finance and facilities teams in practice.

## 2. Utility Data — Portal CSV Export
**Decision:** Accept utility data as a CSV downloaded from the utility provider portal.

**Reason:** PDF parsing is fragile and breaks with every provider's layout change. Utility API availability varies widely by provider and region. CSV export is the standard analyst workflow and is supported by all major UK utility providers.

## 3. Travel Data — Concur CSV Export
**Decision:** Accept travel data as a trip report CSV export from Concur.

**Reason:** Concur's API requires OAuth enterprise setup and IT involvement. The standard analyst workflow is exporting a trip report as CSV — this matches real usage and avoids unnecessary complexity.

## 4. Emission Factors — DEFRA 2023
**Decision:** Use DEFRA 2023 UK Government GHG conversion factors.

**Reason:** DEFRA publishes annually updated, peer-reviewed emission factors that are widely accepted for UK and international corporate reporting. They cover all three scopes required by this assignment.

## 5. Database — SQLite for Development
**Decision:** Use SQLite locally, PostgreSQL on Render for production.

**Reason:** SQLite requires zero configuration and is appropriate for development and demonstration. PostgreSQL is used in production for multi-tenant safety and concurrent access.

## 6. Authentication
**Decision:** Use Django's built-in authentication system.

**Reason:** Sufficient for the analyst review workflow required by this assignment. A production system would add OAuth2 or SSO.