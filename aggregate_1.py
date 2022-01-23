from random import randint
import threading
from time import sleep

TIME_BETWEEN_REQUESTS = 20

lock_temperature = threading.Lock()
lock_presence = threading.Lock()

temperatures = []
presences = []

def send_config_to_slot():
    pass


def temperature_sensor():
    global temperatures
    # TODO connection arduino
    last_temp = 19
    while True:
        # TODO get the temp
        temperature = randint(last_temp - 3, last_temp + 3)
        last_temp = temperature

        lock_temperature.acquire()
        temperatures.append(temperature)
        lock_temperature.release()


def presence_sensor():
    global presences
    # TODO connection arduino
    while True:
        # TODO get the pres
        presence = str(randint(0, 23)) + ":" + str(randint(0, 59))

        lock_presence.acquire()
        presences.append(presence)
        lock_presence.release()


def aggregate():
    global temperatures
    global presences
    
    send_config_to_slot()

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
        temp_prensences = presences.copy()
        presences.clear()
        lock_presence.release()
        
        # TODO send

if __name__ == "__main__":
    # threads
    temperature_sensor_thread = threading.Thread(target=temperature_sensor)
    presence_sensor_thread = threading.Thread(target=presence_sensor)
    aggregate_thread = threading.Thread(target=aggregate)

    # run
    temperature_sensor_thread.start()
    presence_sensor_thread.start()
    aggregate_thread.start()
