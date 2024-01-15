import requests

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "1a6ef8297115d4743cce36a3b48dbc3b"

weather_params = {
    "lat": 53.383331,
    "lon": -1.466667,
    "appid": api_key,
    "units": "metric",
    "cnt": 12,
}

response = requests.get(OWM_Endpoint, params=weather_params)
print(response.json())