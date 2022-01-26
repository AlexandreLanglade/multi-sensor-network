"""
This script simulates a sensor that surveys wifi connections.
He gets the info out of an api and then send it
to the upssitech_slot_api to be store in the database.
"""

from random import randint
from time import sleep, strftime

import requests

API_DEVICE = "https://random-data-api.com/api/device/random_device"
API_SLOT_UPSSITECH = "https://multi-sensor-network-api.ew.r.appspot.com/devices"

if __name__ == "__main__":
    while True:
        # GET request to the random_device api
        device_request = requests.get(API_DEVICE)
        if device_request.status_code == 200:
            # if the request succeeds, look for the model of the device that "connected"
            device_dict = device_request.json()
            device = device_dict["model"]
            device_timestamp = strftime("%d %m %Y %H %M %S")

            # prep of the POST request URL
            str_request = f"{API_SLOT_UPSSITECH}?timestamp={device_timestamp}&device={device}"
            
            # POST request sent to the upssitech_slot_api
            slot_request = requests.post(str_request)

            # print to monitor the request response
            print("-----------------------------")
            print(" ---> POST : " + str_request)
            print(slot_request)
        else:
            print("Error weather API :")
            print(device_request)
        # random time until a new device connection
        random_time = randint(6, 20)
        sleep(random_time)
