import joblib
import pandas as pd

model = joblib.load("model/delay_model.pkl")

def predict_delay(traffic, weather, hour):
    weather_map = {'Clear':0, 'Cloudy':1, 'Rain':2}

    data = pd.DataFrame([[traffic, weather_map[weather], hour]],
                        columns=['traffic_level', 'weather', 'hour'])

    return model.predict(data)[0]

print("Sample Prediction:", predict_delay(6, "Rain", 10))