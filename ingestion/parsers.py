import pandas as pd
import io
from datetime import datetime

EMISSION_FACTORS = {
    'diesel': {'factor': 2.68, 'scope': 1},
    'petrol': {'factor': 2.31, 'scope': 1},
    'natural_gas': {'factor': 2.02, 'scope': 1},
    'electricity': {'factor': 0.207, 'scope': 2},
    'flight': {'factor': 0.255, 'scope': 3},
    'hotel': {'factor': 31.0, 'scope': 3},
    'ground_transport': {'factor': 0.21, 'scope': 3},
}

AIRPORT_DISTANCES = {
    ('BOM', 'LHR'): 7189,
    ('LHR', 'BOM'): 7189,
    ('DEL', 'LHR'): 6700,
    ('JFK', 'LHR'): 5540,
}

def safe_read(file):
    data = file.read()
    if isinstance(data, bytes):
        data = data.decode('utf-8', errors='ignore')
    return pd.read_csv(io.StringIO(data))

def parse_sap(file):
    df = safe_read(file)
    records = []
    for _, row in df.iterrows():
        try:
            desc = str(row.get('MAKTX', '')).lower()
            if 'diesel' in desc or 'kraftstoff' in desc:
                cat = 'diesel'
            elif 'benzin' in desc or 'petrol' in desc:
                cat = 'petrol'
            elif 'erdgas' in desc or 'ngas' in desc:
                cat = 'natural_gas'
            else:
                continue
            ef = EMISSION_FACTORS[cat]
            qty = float(row['MENGE'])
            co2 = round(qty * ef['factor'], 2)
            date_str = str(row['BUDAT'])
            period = date_str[:4] + '-' + date_str[4:6] + '-' + date_str[6:]
            records.append({
                'source_type': 'SAP',
                'scope': ef['scope'],
                'raw_category': str(row.get('MAKTX', '')),
                'raw_value': qty,
                'raw_unit': str(row['MEINS']),
                'period_start': period,
                'period_end': period,
                'normalized_kgco2e': co2,
                'emission_factor': ef['factor'],
                'emission_factor_source': 'DEFRA 2023',
                'flag_reason': 'High value' if co2 > 50000 else '',
            })
        except:
            continue
    return records

def parse_utility(file):
    df = safe_read(file)
    records = []
    for _, row in df.iterrows():
        try:
            kwh = float(row['consumption_kwh'])
            co2 = round(kwh * 0.207, 2)
            records.append({
                'source_type': 'UTILITY',
                'scope': 2,
                'raw_category': 'electricity',
                'raw_value': kwh,
                'raw_unit': 'kWh',
                'period_start': str(row['billing_period_start']),
                'period_end': str(row['billing_period_end']),
                'normalized_kgco2e': co2,
                'emission_factor': 0.207,
                'emission_factor_source': 'DEFRA 2023 UK Grid',
                'flag_reason': '',
            })
        except:
            continue
    return records

def parse_travel(file):
    df = safe_read(file)
    records = []
    for _, row in df.iterrows():
        try:
            cat = str(row['category']).lower()
            if cat == 'flight':
                dist = row.get('distance_km', '')
                if str(dist).strip() == '' or str(dist) == 'nan':
                    key = (str(row.get('origin', '')), str(row.get('destination', '')))
                    dist = AIRPORT_DISTANCES.get(key, 1000)
                dist = float(dist)
                records.append({
                    'source_type': 'TRAVEL',
                    'scope': 3,
                    'raw_category': 'flight',
                    'raw_value': dist,
                    'raw_unit': 'km',
                    'period_start': str(row['travel_date']),
                    'period_end': str(row['travel_date']),
                    'normalized_kgco2e': round(dist * 0.255, 2),
                    'emission_factor': 0.255,
                    'emission_factor_source': 'DEFRA 2023 Aviation',
                    'flag_reason': '',
                })
            elif cat == 'hotel':
                records.append({
                    'source_type': 'TRAVEL',
                    'scope': 3,
                    'raw_category': 'hotel',
                    'raw_value': 1,
                    'raw_unit': 'night',
                    'period_start': str(row['travel_date']),
                    'period_end': str(row['travel_date']),
                    'normalized_kgco2e': 31.0,
                    'emission_factor': 31.0,
                    'emission_factor_source': 'DEFRA 2023 Hotel',
                    'flag_reason': '',
                })
            elif cat == 'ground_transport':
                dist = float(row.get('distance_km', 20))
                records.append({
                    'source_type': 'TRAVEL',
                    'scope': 3,
                    'raw_category': 'ground_transport',
                    'raw_value': dist,
                    'raw_unit': 'km',
                    'period_start': str(row['travel_date']),
                    'period_end': str(row['travel_date']),
                    'normalized_kgco2e': round(dist * 0.21, 2),
                    'emission_factor': 0.21,
                    'emission_factor_source': 'DEFRA 2023 Ground',
                    'flag_reason': '',
                })
        except:
            continue
    return records