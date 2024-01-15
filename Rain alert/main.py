import requests
from twilio.rest import Client
import os

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("MY_API")
account_sid = os.environ.get("MY_SID")
auth_token = os.environ.get("MY_AUTH")

weather_params = {
    "lat": 53.383331,
    "lon": -1.466667,
    "appid": api_key,
    "units": "metric",
    "cnt": 12,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    print("Bring an umbrella.")