import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import pandas as pd

# Charger le modèle Keras
model = tf.keras.models.load_model('static/models/lstm_v1.keras')

app = FastAPI()


class WeatherParams(BaseModel):
    date: datetime.datetime
    temperature_2m: float
    relative_humidity_2m: float
    dew_point_2m: float
    apparent_temperature: float
    precipitation: float
    rain: float
    snowfall: float
    snow_depth: float
    weather_code: int
    pressure_msl: float
    surface_pressure: float
    cloud_cover: float
    cloud_cover_low: float
    cloud_cover_mid: float
    cloud_cover_high: float
    et0_fao_evapotranspiration: float
    vapour_pressure_deficit: float
    wind_speed_10m: float
    wind_speed_100m: float
    wind_direction_10m: float
    wind_direction_100m: float
    wind_gusts_10m: float
    soil_temperature_0_to_7cm: float
    soil_temperature_7_to_28cm: float
    soil_temperature_28_to_100cm: float
    soil_temperature_100_to_255cm: float
    soil_moisture_0_to_7cm: float
    soil_moisture_7_to_28cm: float
    soil_moisture_28_to_100cm: float
    soil_moisture_100_to_255cm: float


@app.post("/predict/")
async def predict(weather: WeatherParams):
    input_data = pd.DataFrame([weather.dict()])
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}
