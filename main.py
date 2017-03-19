import json
import time

import serial
from telegraf.client import TelegrafClient

telegraf_client = TelegrafClient(host='146.185.169.132', port=8092)

serial_client = serial.Serial('/dev/ttyUSB0', baudrate=9600)


def send_data(moisture=0, sensor='Unknown'):
    telegraf_client.metric('moisture', moisture, tags={'location': 'in_home', 'sensor': sensor})


def recv_serial():
    while True:
        raw_data = serial_client.readline()
        print(raw_data)
        data_string = raw_data.decode('utf-8').strip()
        try:
            data = json.loads(data_string)
            yield data
            time.sleep(10)
        except ValueError:
            time.sleep(1)
            pass  # skips one or more datapoints if they cannot be parsed. Especially when the Rasp connect to a running Arduino


if __name__ == "__main__":
    for data in recv_serial():
        for sensor in data:
            send_data(moisture=data[sensor], sensor=sensor)
