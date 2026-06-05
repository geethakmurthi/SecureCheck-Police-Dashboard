import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv(
    "traffic_stops.csv",
    low_memory=False
)

# Clean data
df.dropna(axis=1, how='all', inplace=True)

df.fillna({
    'search_type': 'Unknown',
    'stop_outcome': 'Unknown',
    'driver_age': 0,
    'driver_age_raw': 0,
    'driver_gender': 'Unknown',
    'driver_race': 'Unknown',
    'vehicle_number': 'Unknown'
}, inplace=True)

# Convert date
df['stop_date'] = pd.to_datetime(
    df['stop_date'],
    errors='coerce'
).dt.date

# Convert time
df['stop_time'] = pd.to_datetime(
    df['stop_time'],
    format='%H:%M',
    errors='coerce'
).dt.time

# Database connection
engine = create_engine(
    "postgresql://postgres:geethasri@localhost:5432/police_logs"
)

# Keep only required columns
columns_needed = [
    'stop_date',
    'stop_time',
    'country_name',
    'driver_gender',
    'driver_age_raw',
    'driver_age',
    'driver_race',
    'violation_raw',
    'violation',
    'search_conducted',
    'search_type',
    'stop_outcome',
    'is_arrested',
    'stop_duration',
    'drugs_related_stop',
    'vehicle_number'
]

df = df[columns_needed]

# Upload
df.to_sql(
    'traffic_stops',
    con=engine,
    if_exists='append',
    index=False
)

print("Data uploaded successfully")