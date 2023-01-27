from time import sleep
import datetime

import tinytuya
from pyModbusTCP.client import ModbusClient

from celery import Celery

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def modbus_read_loop():
    bulb_01 = tinytuya.OutletDevice(dev_id='qweqwe', address='f.d.a.195', local_key='qweqwe', version=3.3)  # NOQA
    bulb_02 = tinytuya.OutletDevice(dev_id='qweqwe', address='f.d.a.192', local_key='qweqwe', version=3.3)  # NOQA
    bulb_03 = tinytuya.OutletDevice(dev_id='qweqwe', address='f.d.a.233', local_key='qweqwe', version=3.3)  # NOQA
    bulb_04 = tinytuya.OutletDevice(dev_id='qweqwe', address='f.d.a.115', local_key='qweqwe', version=3.3)  # NOQA
    bulb_05 = tinytuya.OutletDevice(dev_id='qweqwe', address='f.d.a.149', local_key='qweqwe', version=3.3)  # NOQA
    bulb_06 = tinytuya.OutletDevice(dev_id='qwqwe', address='f.d.a.231', local_key='qweqwe', version=3.3)  # NOQA
    bright = 10
    temperature = 0
    while True:

        c = ModbusClient(host="192.168.69.9", auto_open=True, auto_close=True)

        modbus_input_map = c.read_discrete_inputs(1025, 255)
        for pk, val in enumerate(modbus_input_map):
            if val:
                print(pk)
        print(datetime.datetime.now())
        if modbus_input_map[138]:
            bright += 99
            bright = check_limit(bright)
            print('lighter', bright)
            set_light_value(bright, 22, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
        elif modbus_input_map[137]:
            bright -= 99
            bright = check_limit(bright)
            print('darker', bright)
            set_light_value(bright, 22, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
        elif modbus_input_map[136]:
            temperature = temperature + 99
            temperature = check_limit(temperature)
            print('colder', temperature)
            set_light_value(temperature, 23, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
        elif modbus_input_map[135]:
            temperature = temperature - 99
            temperature = check_limit(temperature)
            print('hotter', temperature)
            set_light_value(temperature, 23, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
        sleep(0.05)


def set_light_value(value, index, b1, b2, b3, b4, b5, b6):
    b1.set_value(value=value, index=index)
    b2.set_value(value=value, index=index)
    b3.set_value(value=value, index=index)
    b4.set_value(value=value, index=index)
    b5.set_value(value=value, index=index)
    b6.set_value(value=value, index=index)


def check_limit(value):
    if value > 999:
        value = 999
    if value < 10:
        value = 10
    return value
