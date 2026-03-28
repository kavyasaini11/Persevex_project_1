import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("data/data.csv")

df['scheduled_time'] = pd.to_datetime(df['scheduled_time'], format='%H:%M')
df['actual_time'] = pd.to_datetime(df['actual_time'], format='%H:%M')

df['delay'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

df['weather'] = df['weather'].map({'Clear':0, 'Cloudy':1, 'Rain':2})

X = df[['traffic_level', 'weather', 'hour']]
y = df['delay']

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, "model/delay_model.pkl")

print("✅ Model Ready!")