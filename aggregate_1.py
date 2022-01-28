import json
import threading
from random import randint
from time import sleep, strftime

import requests
import serial
import serial.tools.list_ports

API_SLOT_UPSSITECH = "https://multi-sensor-network-api.ew.r.appspot.com"
TIME_BETWEEN_REQUESTS = 20

arduino_connection = None

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

    while True:
        temperature = randint(16, 28)

        lock_temperature.acquire()
        temperatures.append(temperature)
        lock_temperature.release()
        sleep(2)


def presence_sensor():

    global presences
    someone = False

    while True:
        distance_bytes = arduino_connection.readline()[:-2]
        if distance_bytes:
            distance_str = distance_bytes.decode("utf-8")
            distance_int = int(distance_str[: len(distance_str) - 2])
            if distance_int < 10 and not someone:
                someone = True
                presence = strftime("%d %m %Y %H %M %S")

                lock_presence.acquire()
                presences.append(presence)
                lock_presence.release()
            if distance_int >= 11:
                someone = False


def aggregate():
    global temperatures
    global presences

    send_config_to_slot("aggregate1", "aggregate_1_config.json")

    while True:
        # Send data to the slot every TIME_BETWEEN_REQUESTS seconds
        sleep(TIME_BETWEEN_REQUESTS)
        for i in range(15):
            print("")

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
        mean = sum / len(temp_temperatures)
        mean = round(mean, 1)

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
            slot_request = requests.post(
                f"{API_SLOT_UPSSITECH}/presences?timestamp={element}"
            )
            print(slot_request)
        print("*** Done ***")


if __name__ == "__main__":

    # Connection to Arduino
    ports = serial.tools.list_ports.comports(include_links=False)
    if len(ports) != 0:

        # available ports
        print("Available ports :")
        index = 0
        for port in ports:
            print(str(index) + " : " + port.device)
            index += 1
        port_number = int(input("Port number : "))
        serial_port = ports[port_number].device

        # connection
        arduino_connection = serial.Serial(serial_port, 9600, timeout=1)
        print("Arduino connected.")

    else:
        print("No available port found")

    # threads
    temperature_sensor_thread = threading.Thread(target=temperature_sensor)
    presence_sensor_thread = threading.Thread(target=presence_sensor)
    aggregate_thread = threading.Thread(target=aggregate)

    # run
    temperature_sensor_thread.start()
    presence_sensor_thread.start()
    aggregate_thread.start()
