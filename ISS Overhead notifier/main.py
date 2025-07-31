# import requests
# from datetime import datetime
# import smtplib
# import time
#
# MY_EMAIL = "your email"
# MY_PASSWORD = "your password"
# MY_LAT = 53.381130  # Your latitude
# MY_LONG = -1.470085  # Your longitude
#
#
# def is_iss_overhead():
#     response = requests.get(url="http://api.open-notify.org/iss-now.json")
#     response.raise_for_status()
#     data = response.json()
#
#     iss_latitude = float(data["iss_position"]["latitude"])
#     iss_longitude = float(data["iss_position"]["longitude"])
#
#     # Your position is within +5 or -5 degrees of the ISS position.
#     if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
#         return True
#
#
# def is_night():
#     # sunrise sunset api
#     parameters = {
#         "lat": MY_LAT,
#         "lng": MY_LONG,
#         "formatted": 0
#     }
#     response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
#     response.raise_for_status()
#     data = response.json()
#
#     # sunrise and sunset
#     sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
#     sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
#
#     # current time
#     time_now = datetime.now().hour
#
#     # if time now is greater than sunset or less than sunrise
#     if time_now >= sunset or time_now <= sunrise:
#         return True
#
#
# while True:
#     # if iss is overhead and it is night
#     if is_iss_overhead() and is_night():
#         # send email
#         with smtplib.SMTP("smtp.gmail.com") as connection:
#             connection.starttls()
#             connection.login(user=MY_EMAIL, password=MY_PASSWORD)
#             connection.sendmail(
#                 from_addr=MY_EMAIL,
#                 to_addrs=MY_EMAIL,
#                 msg="Subject:Look Up\n\nThe ISS is above you in the sky."
#             )
#     # check every 60 seconds
#     time.sleep(60)



import requests
from datetime import datetime
import time

MY_LAT = 53.381130  # Your latitude
MY_LONG = -1.470085  # Your longitude

OPENWEATHER_API_KEY = "1a6ef8297115d4743cce36a3b48dbc3b"  # Replace with your OpenWeather API key


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True, iss_latitude, iss_longitude
    return False, iss_latitude, iss_longitude


def is_night():
    # sunrise sunset api
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # sunrise and sunset
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # current time
    time_now = datetime.now().hour

    # if time now is greater than sunset or less than sunrise
    if time_now >= sunset or time_now <= sunrise:
        return True


def get_location_name(lat, lon):
    url = "http://api.openweathermap.org/geo/1.0/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data and "name" in data[0]:
        return data[0]["name"]
    else:
        return "over the ocean"



while True:
    # Check ISS location and overhead status
    iss_overhead, iss_latitude, iss_longitude = is_iss_overhead()

    if iss_overhead and is_night():
        print("Look up! The ISS is above you in the sky.")
    else:
        location_name = get_location_name(iss_latitude, iss_longitude)
        print(f"The ISS is not overhead right now. "
              f"Current overhead location is {location_name} (Latitude: {iss_latitude}, Longitude: {iss_longitude}).")
    # check every 60 seconds
    time.sleep(60)
