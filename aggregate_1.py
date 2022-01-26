from random import randint
import threading
from time import sleep, strftime
import json
import requests

API_SLOT_UPSSITECH = "https://multi-sensor-network-api.ew.r.appspot.com"
TIME_BETWEEN_REQUESTS = 20

lock_temperature = threading.Lock()
lock_presence = threading.Lock()

temperatures = []
presences = []

def send_config_to_slot(name, path):
    with open(path) as config_file:
        config = json.load(config_file)
    
    config["name_aggregate"] = name

    str_request = f"{API_SLOT_UPSSITECH}/aggregates"

    # POST request sent to the upssitech_slot_api
    print("*** Sending aggregate's config to the slot ***")
    slot_request = requests.post(str_request, json=config)
    print(" ---> POST : " + str_request)
    print(slot_request)
    print("*** Done ***")

def temperature_sensor():
    global temperatures
    # TODO connection arduino
    last_temp = 19
    while True:
        # TODO get the temp (int)
        temperature = randint(last_temp - 3, last_temp + 3)
        last_temp = temperature

        lock_temperature.acquire()
        temperatures.append(temperature)
        lock_temperature.release()


def presence_sensor():
    global presences
    # TODO connection arduino
    while True:
        # TODO get the pres strftime("%d %m %Y %H %M %S")
        p = randint(0,100)
        if p > 96:
            print("coucou")
            presence = strftime("%d %m %Y %H %M %S")

            lock_presence.acquire()
            presences.append(presence)
            lock_presence.release()


def aggregate():
    global temperatures
    global presences
    
    send_config_to_slot("aggregate1","aggregate_1_config.json")

    while True:
        # Send data to the slot every TIME_BETWEEN_REQUESTS seconds
        sleep(TIME_BETWEEN_REQUESTS)

        # Get data from the temperature sensor
        lock_temperature.acquire()
        temp_temperatures = temperatures.copy()
        temperatures.clear()
        lock_temperature.release()

        # Get data from the presence sensor
        lock_presence.acquire()
        temp_presences = presences.copy()
        presences.clear()
        lock_presence.release()

        # Calculate average temperature
        sum = 0
        for element in temp_temperatures:
            sum += element
        mean = sum/len(temp_temperatures)
        mean = round(mean,1)
        
        timestamp = strftime("%d %m %Y %H %M %S")

        # Send temperature data to the slot
        str_request = f"{API_SLOT_UPSSITECH}/temperatures?timestamp={timestamp}&temperature={mean}"
        print("*** Sending temperature data to the slot ***")
        slot_request = requests.post(str_request)
        print(" ---> POST : " + str_request)
        print(slot_request)
        print("*** Done ***")

        # Send presence data to the slot
        print("*** Sending presence data to the slot ***")
        for element in temp_presences:
            slot_request = requests.post(f"{API_SLOT_UPSSITECH}/presences?timestamp={element}")
            print(slot_request)
        print("*** Done ***")



if __name__ == "__main__":
    
    # threads
    temperature_sensor_thread = threading.Thread(target=temperature_sensor)
    presence_sensor_thread = threading.Thread(target=presence_sensor)
    aggregate_thread = threading.Thread(target=aggregate)

    # run
    #temperature_sensor_thread.start()
    #presence_sensor_thread.start()
    aggregate_thread.start()
