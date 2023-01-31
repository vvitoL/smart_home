import os
from time import sleep
import datetime

import tinytuya
from pyModbusTCP.client import ModbusClient

from celery import Celery
from dotenv import load_dotenv

load_dotenv()
app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def modbus_read_loop():
    bulb_01 = tinytuya.OutletDevice(dev_id=os.getenv("B1_ID"), address=os.getenv("B1_IP"), local_key=os.getenv("B1_KEY"), version=3.3)  # NOQA
    bulb_02 = tinytuya.OutletDevice(dev_id=os.getenv("B2_ID"), address=os.getenv("B2_IP"), local_key=os.getenv("B2_KEY"), version=3.3)  # NOQA
    bulb_03 = tinytuya.OutletDevice(dev_id=os.getenv("B3_ID"), address=os.getenv("B3_IP"), local_key=os.getenv("B3_KEY"), version=3.3)  # NOQA
    bulb_04 = tinytuya.OutletDevice(dev_id=os.getenv("B4_ID"), address=os.getenv("B4_IP"), local_key=os.getenv("B4_KEY"), version=3.3)  # NOQA
    bulb_05 = tinytuya.OutletDevice(dev_id=os.getenv("B5_ID"), address=os.getenv("B5_IP"), local_key=os.getenv("B5_KEY"), version=3.3)  # NOQA
    bulb_06 = tinytuya.OutletDevice(dev_id=os.getenv("B6_ID"), address=os.getenv("B6_IP"), local_key=os.getenv("B6_KEY"), version=3.3)  # NOQA
    bright = 10
    temperature = 0
    while True:

        try:
            c = ModbusClient(host=os.getenv("PLC_IP"), auto_open=True, auto_close=True)
            modbus_input_map = c.read_discrete_inputs(1025, 255)
            for pk, val in enumerate(modbus_input_map):
                if val:
                    print(pk)

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
                temperature += 99
                temperature = check_limit(temperature)
                print('colder', temperature)
                set_light_value(temperature, 23, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
            elif modbus_input_map[135]:
                temperature -= 99
                temperature = check_limit(temperature)
                print('hotter', temperature)
                set_light_value(temperature, 23, bulb_01, bulb_02, bulb_03, bulb_04, bulb_05, bulb_06)
            else:
                sleep(0.1)
        except TypeError:
            print("PLC disconnected")
            sleep(0.5)

        print(datetime.datetime.now())


def set_light_value(value, index, b1, b2, b3, b4, b5, b6):
    sleep(0.02)
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
