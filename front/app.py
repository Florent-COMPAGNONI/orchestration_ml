import streamlit as st
import requests
import pandas as pd
import time

# Define the API URL
API_URL = "https://weather-api-cv3s3i6o4q-od.a.run.app/predict/"


def fetch_temperature_data():
    """Fetches temperature data from the API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API")
        return []


def main():
    st.title('Temperature Predictions for Today')

    # Fetching temperature data from the API
    fetch = fetch_temperature_data()

    if isinstance(fetch, list):
        temperatures = fetch.get('temperatures')
    else:
        temperatures = [round(float(temp)) for temp in
                        fetch.get('predictions').replace("[", "").replace("]", "").replace(" ", "").split(",")]

    if temperatures:
        # Creating a DataFrame for visualization
        df = pd.DataFrame({
            'Hour': range(len(temperatures)),
            'Temperature': temperatures
        })

        hour = st.sidebar.slider("hour", 0, 23)
        hour_to_string = hour % 12
        hour_string = "12" if hour_to_string == 0 else str(hour_to_string)
        hour_string = hour_string + ' pm' if hour > 11 else hour_string + ' am'

        st.header('Look close by hour', divider='rainbow')
        st.subheader(f"At {hour_string} :sunglasses:")
        temp = temperatures[hour]
        st.markdown(f"The temperature should be at ***{temp} °C***")

        st.header('About today\'s temperature', divider='rainbow')
        st.subheader('Line Chart of Temperatures')
        st.line_chart(data=df.set_index('Hour'), y_label="Temperature", x_label="Hour")

        # Adding a bar chart
        st.subheader('Bar Chart of Temperatures')
        st.bar_chart(df.set_index('Hour'), y_label="Temperature", x_label="Hour")


if __name__ == "__main__":
    main()
