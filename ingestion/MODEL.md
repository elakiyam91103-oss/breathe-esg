# Data Model Documentation

## Overview
The Breathe ESG platform uses a relational data model designed around four core entities: Client, DataIngestion, EmissionRecord, and AuditLog.

## Entity Relationship

Client (tenant)
  └── DataIngestion (one upload event)
        └── EmissionRecord (one normalized row)
              └── AuditLog (every status change)

## Entities

### Client
Represents a company using the platform.
- id, name, created_at

### DataIngestion
Represents one CSV upload event.
- client, source_type (SAP/UTILITY/TRAVEL)
- uploaded_at, file_name, row_count, error_count

### EmissionRecord
The core entity — one row of normalized emissions data.
- client, ingestion (links to upload)
- source_type, scope (1, 2, or 3)
- raw_category, raw_value, raw_unit (what came in)
- normalized_kgco2e (converted value)
- emission_factor, emission_factor_source
- status (PENDING / APPROVED / FLAGGED / REJECTED)
- flag_reason, reviewed_by, reviewed_at
- is_locked (prevents edits after audit sign-off)

### AuditLog
Records every status change on an EmissionRecord.
- record, changed_by, changed_at
- field_changed, old_value, new_value

## Key Design Decisions
- raw_value and raw_unit are stored alongside normalized_kgco2e so the original data is never lost
- emission_factor_source is stored per record so future factor updates don't silently change historical data
- is_locked prevents any edits after an auditor signs off
- scope is stored as an integer (1, 2, 3) matching GHG Protocol categories