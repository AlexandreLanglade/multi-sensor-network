"""
This script simulates a weather-observing sensor.
He gets the info out of an api and then send it
to the upssitech_slot_api to be store in the database.
It does it every TIME_BETWEEN_REQUESTS seconds.
"""

from random import randint
from time import sleep

import requests

API_WEATHER = "https://www.metaweather.com/api/location/628886/"
API_SLOT_UPSSITECH = "https://multi-sensor-network-api.ew.r.appspot.com/weathers"
TIME_BETWEEN_REQUESTS = 10

if __name__ == "__main__":
    while True:
        # GET request to the weather api
        weather_request = requests.get(API_WEATHER)
        if weather_request.status_code == 200:
            # if the request succeeds, look for the weather state and the temperature
            weather_dict = weather_request.json()["consolidated_weather"][0]
            weather_state_name = weather_dict["weather_state_name"]
            weather_temperature = int(weather_dict["the_temp"])
            weather = str(weather_temperature) + "°C : " + weather_state_name
            # it's a simulation and the id doesn't really matter here then it is choose randomly
            random_id = str(randint(1000, 100000))
            # prep of the POST request URL
            str_request = (
                API_SLOT_UPSSITECH + "?weatherId=" + random_id + "&weather=" + weather
            )
            # POST request sent to the upssitech_slot_api
            slot_request = requests.post(str_request)
            # print to monitor the request response
            print("-----------------------------")
            print(" ---> POST : " + str_request)
            print(slot_request)
        else:
            print("Error weather API :")
            print(weather_request)
        sleep(TIME_BETWEEN_REQUESTS)
