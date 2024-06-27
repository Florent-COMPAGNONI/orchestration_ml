import datetime

from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
from pydantic import BaseModel
import tensorflow as tf
import pandas as pd

# Charger le modèle Keras
model = tf.keras.models.load_model("/app/static/models/lstm_v1.keras")
scaler_features = joblib.load("/app/static/scalers/scaler_features_v1.pkl")
scaler_target = joblib.load("/app/static/scalers/scaler_target_v1.pkl")

app = FastAPI()


# class WeatherParams(BaseModel):
#     date: datetime.datetime
#     temperature_2m: float
#     relative_humidity_2m: float
#     dew_point_2m: float
#     apparent_temperature: float
#     precipitation: float
#     rain: float
#     snowfall: float
#     snow_depth: float
#     weather_code: int
#     pressure_msl: float
#     surface_pressure: float
#     cloud_cover: float
#     cloud_cover_low: float
#     cloud_cover_mid: float
#     cloud_cover_high: float
#     et0_fao_evapotranspiration: float
#     vapour_pressure_deficit: float
#     wind_speed_10m: float
#     wind_speed_100m: float
#     wind_direction_10m: float
#     wind_direction_100m: float
#     wind_gusts_10m: float
#     soil_temperature_0_to_7cm: float
#     soil_temperature_7_to_28cm: float
#     soil_temperature_28_to_100cm: float
#     soil_temperature_100_to_255cm: float
#     soil_moisture_0_to_7cm: float
#     soil_moisture_7_to_28cm: float
#     soil_moisture_28_to_100cm: float
#     soil_moisture_100_to_255cm: float


# Helper function to prepare data for prediction
def prepare_data(features, scaler_features, time_step=24):
    # features_scaled = scaler_features.transform(features)
    X = []
    for i in range(len(features) - time_step + 1):
        X.append(features[i : (i + time_step), :])
    return np.array(X)


def get_file_path(local=False):
    if local:
        return "weather_data_2024_06_25.csv"
    return "/app/weather_data_2024_06_25.csv"


@app.get("/predict/")
async def predict():
    file_path = get_file_path()

    # Read the CSV file
    features = pd.read_csv(file_path)

    # Convert date column to datetime
    features["date"] = pd.to_datetime(features["date"])

    # Set date as index
    features.set_index("date", inplace=True)

    # Drop the date column as it's not used in prediction
    features.drop(columns=["temperature_2m"], inplace=True)

    features["snow_depth"] = 0.0
    if features.isnull().values.any():
        features.fillna(features.mean(), inplace=True)

    if features.isnull().values.any():
        raise HTTPException(status_code=400, detail="NaN values")

    if features.shape[0] != 24:
        raise HTTPException(
            status_code=400, detail="CSV file must contain exactly 24 rows"
        )

    time_step = 24  # This should match the time_step used during training

    time_step = 24  # This should match the time_step used during training
    predictions = []

    for _ in range(24):
        X = prepare_data(features.values, scaler_features, time_step)
        if X.size == 0:
            raise HTTPException(
                status_code=400, detail="Not enough data to make predictions"
            )

        y_pred_scaled = model.predict(X)
        y_pred_value = y_pred_scaled.flatten().tolist()[0] * 100

        # Append the prediction to the list of predictions
        predictions.append(y_pred_value)

        # Update the features DataFrame to include the new predicted temperature
        new_row = features.iloc[-1].copy()
        # new_row["temperature_2m"] = y_pred_value
        new_row_df = pd.DataFrame(new_row).transpose()
        features = pd.concat([features, new_row_df], ignore_index=True)
        features = features.iloc[
            1:
        ]  # Remove the oldest row to maintain the window size of 24

    return {"predictions": predictions}
