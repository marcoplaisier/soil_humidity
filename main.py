import json

import serial
from telegraf.client import TelegrafClient

TELEGRAF_HOST = '146.185.169.132'
TELEGRAF_PORT = 8092
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUD_RATE = 9600


def convert_to_json(raw_data):
    text_data = raw_data.decode('utf-8').strip()
    return json.loads(text_data)


def send_data(client, value=0, sensor_type='', sensor='unknown'):
    client.metric(sensor_type, value, tags={'sensor': sensor})


def recv_serial(client):
    while True:
        raw_data = client.readline()  # blocking call, due to serial.Serial(...) with timeout=None
        try:
            json_data = convert_to_json(raw_data)
            assert json_data['value'] 
            assert json_data['sensor_type']
            assert json_data['sensor']
            yield json_data
        except ValueError:
            pass  # when the Rasp connects to a running Arduino which has already sent data via serial, data is corrupt


def main_loop(output_client, input_client):
    for sensors in recv_serial(client=input_client):
        for sensor_data in sensors:
            send_data(client=output_client, **sensor_data)


if __name__ == "__main__":
    telegraf_client = TelegrafClient(host=TELEGRAF_HOST, port=TELEGRAF_PORT)
    serial_client = serial.Serial(SERIAL_PORT, baudrate=SERIAL_BAUD_RATE, timeout=None)

    main_loop(telegraf_client, serial_client)
