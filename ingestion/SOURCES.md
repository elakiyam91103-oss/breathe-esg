# Sources and References

## Emission Factors

| Source | Used For | URL |
|--------|----------|-----|
| DEFRA 2023 UK GHG Conversion Factors | Diesel, Petrol, Natural Gas, Electricity, Aviation, Hotel, Ground Transport | https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2023 |

### Specific Factors Used
| Category | Factor | Unit | Scope |
|----------|--------|------|-------|
| Diesel | 2.68 kg CO₂e | per litre | Scope 1 |
| Petrol | 2.31 kg CO₂e | per litre | Scope 1 |
| Natural Gas | 2.02 kg CO₂e | per m³ | Scope 1 |
| UK Electricity | 0.207 kg CO₂e | per kWh | Scope 2 |
| Flight (economy) | 0.255 kg CO₂e | per km | Scope 3 |
| Hotel (UK) | 31.0 kg CO₂e | per night | Scope 3 |
| Ground Transport | 0.21 kg CO₂e | per km | Scope 3 |

## Standards and Frameworks

| Standard | Purpose |
|----------|---------|
| GHG Protocol Corporate Standard | Defines Scope 1, 2, 3 classification |
| DEFRA Environmental Reporting Guidelines 2019 | Guidance on what to measure and report |

## Airport Distance Data
Distances between airport pairs (BOM-LHR, DEL-LHR, JFK-LHR) sourced from Great Circle Mapper (gcmap.com) and used where flight distance is not provided in the source data.

## Technology

| Library | Version | Purpose |
|---------|---------|---------|
| Django | 6.0.5 | Backend web framework |
| Django REST Framework | 3.17.1 | REST API |
| pandas | 3.0.3 | CSV parsing and data manipulation |
| React | 18 | Frontend dashboard |
| axios | latest | HTTP requests from React to Django |