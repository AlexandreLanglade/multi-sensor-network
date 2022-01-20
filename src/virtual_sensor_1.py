from random import randint
from time import sleep

import requests

API_METEO = "https://www.metaweather.com/api/location/628886/"
API_SLOT_UPSSITECH = "https://multi-sensor-network-api.ew.r.appspot.com/weathers"

if __name__ == "__main__":
    while True:
        weather_request = requests.get(API_METEO)
        if weather_request.status_code == 200:
            weather_dict = weather_request.json()["consolidated_weather"][0]
            weather_state_name = weather_dict["weather_state_name"]
            weather_temperature = int(weather_dict["the_temp"])
            weather = str(weather_temperature) + "°C : " + weather_state_name
            random_id = str(randint(1000, 10000))  # TODO delete doc firestore
            str_request = (
                API_SLOT_UPSSITECH + "?weatherId=" + random_id + "&weather=" + weather
            )
            slot_request = requests.post(str_request)
            print("-----------------------------")
            print(" ---> POST : " + str_request)
            print(slot_request)
        else:
            print("Error weather API :")
            print(weather_request)
        sleep(10)
