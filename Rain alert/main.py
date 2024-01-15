import requests
from twilio.rest import Client
import os

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("MY_API")
account_sid = os.environ.get("MY_SID")
auth_token = os.environ.get("MY_AUTH")
my_number = os.environ.get("MY_NUMBER")
twilio_number = os.environ.get("TWILIO_NUMBER")

weather_params = {
    "lat": -10.686260,
    "lon": -77.774567,
    "appid": api_key,
    "cnt": 4,
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
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☂️",
        from_=twilio_number,
        to=my_number
    )
    print(message.status)
