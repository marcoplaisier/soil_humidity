import json
import time

import serial
from telegraf.client import TelegrafClient

telegraf_client = TelegrafClient(host='146.185.169.132', port=8092)


serial_client = serial.Serial('/dev/ttyUSB0', baudrate=9600)


def send_data(moisture=0, sensor='Unknown'):
    telegraf_client.metric('soil_moisture', moisture, tags={'location': 'schuur', 'sensor': sensor})


def recv_serial():
    while True:
        raw_data = serial_client.readline()
        data = json.loads(raw_data)
        yield data
        time.sleep(10)


if __name__ == "__main__":
    for data in recv_serial():
        for sensor in data:
            send_data(moisture=data[sensor], sensor=sensor)
