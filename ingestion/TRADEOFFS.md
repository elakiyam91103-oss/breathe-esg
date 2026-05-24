# Tradeoffs

## 1. CSV vs API Integration
**Chose:** CSV file upload
**Trade-off:** Loses real-time data; requires manual analyst export step
**Why accepted:** API integrations require enterprise credentials and IT access not available to an ingestion service. CSV covers 95% of real analyst workflows.

## 2. SQLite vs PostgreSQL (local)
**Chose:** SQLite for local development
**Trade-off:** Not suitable for concurrent users or large datasets
**Why accepted:** Simplifies setup for demonstration. PostgreSQL is used on Render in production.

## 3. Rule-based category detection vs ML classification
**Chose:** Rule-based keyword matching (e.g. "diesel", "kraftstoff")
**Trade-off:** Will miss unusual material descriptions not in the ruleset
**Why accepted:** Rule-based is transparent, auditable, and explainable — important for ESG compliance. ML classification is a black box which auditors cannot verify.

## 4. DEFRA 2023 fixed factors vs real-time factor lookup
**Chose:** Hardcoded DEFRA 2023 factors stored per record
**Trade-off:** Requires manual update when DEFRA publishes new factors annually
**Why accepted:** Storing the factor used at ingestion time preserves audit integrity. If factors were looked up dynamically, historical records would silently change when factors are updated — unacceptable for regulated reporting.

## 5. Single-tenant UI vs full multi-tenancy
**Chose:** Single default client for demonstration
**Trade-off:** Does not demonstrate full tenant isolation in the UI
**Why accepted:** The data model fully supports multi-tenancy (every record has a client foreign key). UI multi-tenancy is an implementation detail beyond the assignment scope.