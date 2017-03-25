import json
import time

import serial
from telegraf.client import TelegrafClient

telegraf_client = TelegrafClient(host='146.185.169.132', port=8092)

serial_client = serial.Serial('/dev/ttyUSB0', baudrate=9600)


def send_data(value=0, type='moisture', sensor='Unknown'):
    telegraf_client.metric(type, value, tags={'location': 'in_home', 'sensor': sensor})


def recv_serial():
    while True:
        raw_data = serial_client.readline()
        data_string = raw_data.decode('utf-8').strip()
        try:
            data = json.loads(data_string)
            yield data
            time.sleep(10)
        except ValueError:
            time.sleep(1)
            pass  # skips one or more lines if they cannot be parsed
            # happens when the Rasp connects to a running Arduino which has already sent data


if __name__ == "__main__":
    for data in recv_serial():
        for sensor in data:
            if sensor.startswith("luminosity"):
                send_data(value=data[sensor], type='light', sensor='light_sensor')
            else:
                sensor_name = "moisture_" + sensor
                send_data(value=data[sensor], type='moisture', sensor=sensor_name)
